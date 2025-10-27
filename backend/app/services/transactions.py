"""
Transaction Management & Data Consistency
FIX #9: Atomic Transactions

Ensures data integrity across multiple database operations
"""

from sqlalchemy.orm import Session
from contextlib import contextmanager
from typing import Optional, Callable, Any
import logging

logger = logging.getLogger(__name__)


class TransactionManager:
    """Manages database transactions with proper rollback handling"""
    
    @staticmethod
    @contextmanager
    def atomic_transaction(db: Session, operation_name: str = "Operation"):
        """
        Execute code within an atomic transaction
        
        Usage:
            with TransactionManager.atomic_transaction(db, "create_user_and_subscription"):
                # All operations here are atomic
                user = create_user(db, ...)
                subscription = create_subscription(db, user_id=user.id, ...)
                # If any fails, both are rolled back
        """
        try:
            logger.info(f"🔄 Starting transaction: {operation_name}")
            yield db
            
            # Flush changes to DB (but don't commit yet)
            db.flush()
            logger.info(f"✅ Transaction flushed: {operation_name}")
            
            # Commit if everything succeeded
            db.commit()
            logger.info(f"✅ Transaction committed: {operation_name}")
            
        except Exception as e:
            # Rollback on any error
            db.rollback()
            logger.error(f"❌ Transaction rolled back: {operation_name} - {str(e)}")
            raise
    
    @staticmethod
    def savepoint_transaction(db: Session, savepoint_name: str = "sp1"):
        """
        Create a savepoint within a transaction
        
        Usage:
            with db.begin_nested():  # Creates savepoint
                # Do some operations
                db.flush()
                # If error here, only this savepoint rolls back
        """
        return db.begin_nested()
    
    @staticmethod
    def execute_with_retry(
        db: Session,
        operation: Callable,
        max_retries: int = 3,
        operation_name: str = "Operation"
    ) -> Optional[Any]:
        """
        Execute operation with retry logic for transient failures
        
        Args:
            db: Database session
            operation: Callable that performs the operation
            max_retries: Number of retry attempts
            operation_name: Name for logging
        
        Returns:
            Result from operation
        """
        from time import sleep
        
        for attempt in range(max_retries):
            try:
                logger.info(f"🔄 Attempt {attempt+1}/{max_retries}: {operation_name}")
                result = operation()
                logger.info(f"✅ Success: {operation_name}")
                return result
            
            except Exception as e:
                if attempt < max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s
                    wait_time = 2 ** attempt
                    logger.warning(
                        f"⚠️  {operation_name} failed (attempt {attempt+1}), "
                        f"retrying in {wait_time}s: {str(e)}"
                    )
                    sleep(wait_time)
                    db.rollback()
                else:
                    logger.error(f"❌ Failed after {max_retries} attempts: {operation_name}")
                    raise
    
    @staticmethod
    def batch_operation(
        db: Session,
        items: list,
        operation: Callable,
        batch_size: int = 100,
        operation_name: str = "Batch Operation"
    ) -> tuple:
        """
        Execute operation on batches of items with transactional integrity
        
        Args:
            db: Database session
            items: Items to process
            operation: Callable to execute on each batch
            batch_size: Items per batch
            operation_name: Name for logging
        
        Returns:
            (successful_count, failed_count)
        """
        successful = 0
        failed = 0
        
        # Process in batches
        for i in range(0, len(items), batch_size):
            batch = items[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            try:
                with TransactionManager.atomic_transaction(
                    db, f"{operation_name} Batch {batch_num}"
                ):
                    for item in batch:
                        operation(db, item)
                    successful += len(batch)
                    logger.info(
                        f"✅ Batch {batch_num} complete: {len(batch)} items processed"
                    )
            
            except Exception as e:
                failed += len(batch)
                logger.error(f"❌ Batch {batch_num} failed: {str(e)}")
                # Continue with next batch instead of failing entire operation
        
        logger.info(f"📊 {operation_name} complete: {successful} success, {failed} failed")
        return successful, failed


class TransactionalDecorator:
    """Decorator for automatic transaction management"""
    
    @staticmethod
    def transactional(operation_name: str = "Operation"):
        """
        Decorator to wrap function in automatic transaction
        
        Usage:
            @TransactionalDecorator.transactional("create_invoice")
            def create_invoice(db: Session, invoice_data: dict) -> Invoice:
                # Function body
                return invoice
        """
        def decorator(func):
            def wrapper(*args, db: Session = None, **kwargs):
                if db is None:
                    raise ValueError("db Session required in kwargs")
                
                with TransactionManager.atomic_transaction(db, operation_name):
                    return func(*args, db=db, **kwargs)
            
            return wrapper
        return decorator
    
    @staticmethod
    def read_only():
        """
        Decorator for read-only operations (no transaction needed)
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                # Read-only, no commit needed
                return result
            return wrapper
        return decorator


# Example: Payment transaction (atomic across multiple tables)
def process_payment_transaction(
    db: Session,
    user_id: str,
    amount: float,
    razorpay_payment_id: str
) -> dict:
    """
    Process payment with full transactional integrity
    
    All operations below are atomic - if ANY fail, ALL are rolled back
    """
    from app.models import Subscription, PaymentRecord, UsageLog
    from datetime import datetime
    
    with TransactionManager.atomic_transaction(db, f"Payment for {user_id}"):
        # Step 1: Create payment record
        payment = PaymentRecord(
            user_id=user_id,
            amount=amount,
            razorpay_payment_id=razorpay_payment_id,
            status="completed",
            created_at=datetime.utcnow()
        )
        db.add(payment)
        db.flush()  # Flush to get payment ID
        
        # Step 2: Update subscription (or create new one)
        subscription = db.query(Subscription).filter_by(user_id=user_id).first()
        if subscription:
            subscription.status = "active"
            subscription.scans_used_this_period = 0
        else:
            subscription = Subscription(
                user_id=user_id,
                tier="pro",
                status="active",
                scans_used_this_period=0
            )
            db.add(subscription)
        db.flush()
        
        # Step 3: Log usage
        usage = UsageLog(
            user_id=user_id,
            operation_type="payment",
            description=f"Payment of {amount} processed",
            timestamp=datetime.utcnow()
        )
        db.add(usage)
        db.flush()
        
        # If we reach here, all operations succeeded
        # All are committed together
        
        return {
            "payment_id": payment.id,
            "subscription_id": subscription.id,
            "status": "success"
        }


# Example: Batch invoice processing
def batch_process_invoices(
    db: Session,
    invoice_ids: list,
    processor_func: Callable
) -> tuple:
    """
    Process multiple invoices with batch transactions
    """
    def process_invoice(db: Session, invoice_id: str):
        from app.models import Invoice
        invoice = db.query(Invoice).filter_by(id=invoice_id).first()
        if invoice:
            processor_func(db, invoice)
    
    return TransactionManager.batch_operation(
        db,
        invoice_ids,
        process_invoice,
        batch_size=50,
        operation_name="Invoice Processing"
    )


if __name__ == "__main__":
    print("✅ Transaction Management module loaded")
    print("\nUsage examples:")
    print("1. with TransactionManager.atomic_transaction(db, 'operation'):")
    print("2. @TransactionalDecorator.transactional('operation_name')")
    print("3. TransactionManager.execute_with_retry(db, operation_func)")
    print("4. TransactionManager.batch_operation(db, items, processor)")
