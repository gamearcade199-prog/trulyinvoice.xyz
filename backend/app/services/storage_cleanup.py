"""
Storage Cleanup Service
Automatically removes old invoices and documents based on subscription tier
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List
import logging

from app.services.supabase_helper import supabase
from app.config.plans import get_storage_days

logger = logging.getLogger(__name__)


class StorageCleanupService:
    """Service for cleaning up old data based on subscription tiers"""
    
    @staticmethod
    def cleanup_user_data(user_id: str, tier: str) -> Dict[str, int]:
        """
        Clean up old data for a specific user based on their subscription tier
        
        Args:
            user_id: User ID to clean up data for
            tier: User's subscription tier (free, basic, pro, ultra, max)
        
        Returns:
            Dictionary with counts of deleted documents and invoices
        """
        try:
            # Get storage retention days for the user's tier
            retention_days = get_storage_days(tier)
            
            if retention_days <= 0:
                logger.info(f"Tier {tier} has unlimited storage, skipping cleanup")
                return {"documents_deleted": 0, "invoices_deleted": 0}
            
            # Calculate cutoff date
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            cutoff_iso = cutoff_date.isoformat()
            
            logger.info(f"Cleaning up data for user {user_id} (tier: {tier}, retention: {retention_days} days)")
            logger.info(f"Deleting documents older than: {cutoff_iso}")
            
            # Get old documents
            old_documents = supabase.table("documents").select("id").eq("user_id", user_id).lt("created_at", cutoff_iso).execute()
            
            documents_deleted = 0
            invoices_deleted = 0
            
            if old_documents.data:
                document_ids = [doc["id"] for doc in old_documents.data]
                
                # Delete associated invoices first (foreign key constraint)
                for doc_id in document_ids:
                    invoice_result = supabase.table("invoices").delete().eq("document_id", doc_id).execute()
                    if invoice_result.data:
                        invoices_deleted += len(invoice_result.data)
                
                # Delete documents
                for doc_id in document_ids:
                    doc_result = supabase.table("documents").delete().eq("id", doc_id).execute()
                    if doc_result.data:
                        documents_deleted += len(doc_result.data)
                
                logger.info(f"✅ Cleanup complete: {documents_deleted} documents, {invoices_deleted} invoices deleted")
            else:
                logger.info(f"No old documents found for user {user_id}")
            
            return {
                "documents_deleted": documents_deleted,
                "invoices_deleted": invoices_deleted,
                "retention_days": retention_days,
                "cutoff_date": cutoff_iso
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up data for user {user_id}: {e}")
            return {"documents_deleted": 0, "invoices_deleted": 0, "error": str(e)}
    
    
    @staticmethod
    def cleanup_all_users() -> Dict[str, any]:
        """
        Clean up old data for all users based on their subscription tiers
        
        Returns:
            Dictionary with cleanup statistics
        """
        try:
            logger.info("🧹 Starting storage cleanup for all users...")
            
            # Get all users with their subscription tiers
            subscriptions = supabase.table("subscriptions").select("user_id, tier, status").execute()
            
            if not subscriptions.data:
                logger.info("No subscriptions found")
                return {"total_users": 0, "users_cleaned": 0}
            
            total_documents_deleted = 0
            total_invoices_deleted = 0
            users_cleaned = 0
            errors = []
            
            for subscription in subscriptions.data:
                user_id = subscription.get("user_id")
                tier = subscription.get("tier", "free")
                status = subscription.get("status", "active")
                
                # Only cleanup for active subscriptions
                if status != "active":
                    logger.info(f"Skipping user {user_id} - subscription not active")
                    continue
                
                try:
                    result = StorageCleanupService.cleanup_user_data(user_id, tier)
                    
                    if "error" not in result:
                        total_documents_deleted += result.get("documents_deleted", 0)
                        total_invoices_deleted += result.get("invoices_deleted", 0)
                        users_cleaned += 1
                    else:
                        errors.append(f"User {user_id}: {result['error']}")
                        
                except Exception as e:
                    logger.error(f"Error processing user {user_id}: {e}")
                    errors.append(f"User {user_id}: {str(e)}")
            
            logger.info(f"✅ Storage cleanup complete!")
            logger.info(f"   Users processed: {users_cleaned}/{len(subscriptions.data)}")
            logger.info(f"   Documents deleted: {total_documents_deleted}")
            logger.info(f"   Invoices deleted: {total_invoices_deleted}")
            
            return {
                "total_users": len(subscriptions.data),
                "users_cleaned": users_cleaned,
                "total_documents_deleted": total_documents_deleted,
                "total_invoices_deleted": total_invoices_deleted,
                "errors": errors,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in cleanup_all_users: {e}")
            return {
                "total_users": 0,
                "users_cleaned": 0,
                "error": str(e)
            }
    
    
    @staticmethod
    def cleanup_anonymous_uploads() -> Dict[str, int]:
        """
        Clean up anonymous uploads older than 24 hours
        
        Returns:
            Dictionary with counts of deleted items
        """
        try:
            logger.info("🧹 Cleaning up anonymous uploads...")
            
            # Delete documents older than 24 hours with no user_id
            cutoff_date = (datetime.utcnow() - timedelta(hours=24)).isoformat()
            
            # Get old anonymous documents
            old_docs = supabase.table("documents").select("id").is_("user_id", "null").lt("created_at", cutoff_date).execute()
            
            documents_deleted = 0
            invoices_deleted = 0
            
            if old_docs.data:
                document_ids = [doc["id"] for doc in old_docs.data]
                
                # Delete invoices first
                for doc_id in document_ids:
                    invoice_result = supabase.table("invoices").delete().eq("document_id", doc_id).execute()
                    if invoice_result.data:
                        invoices_deleted += len(invoice_result.data)
                
                # Delete documents
                for doc_id in document_ids:
                    doc_result = supabase.table("documents").delete().eq("id", doc_id).execute()
                    if doc_result.data:
                        documents_deleted += len(doc_result.data)
                
                logger.info(f"✅ Anonymous cleanup: {documents_deleted} documents, {invoices_deleted} invoices deleted")
            
            return {
                "documents_deleted": documents_deleted,
                "invoices_deleted": invoices_deleted,
                "cutoff_date": cutoff_date
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up anonymous uploads: {e}")
            return {"documents_deleted": 0, "invoices_deleted": 0, "error": str(e)}
    
    
    @staticmethod
    def get_storage_stats(user_id: str) -> Dict[str, any]:
        """
        Get storage statistics for a user
        
        Args:
            user_id: User ID to get stats for
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            # Get user's documents
            documents = supabase.table("documents").select("id, created_at, file_size").eq("user_id", user_id).execute()
            
            if not documents.data:
                return {
                    "total_documents": 0,
                    "total_storage_bytes": 0,
                    "oldest_document": None,
                    "newest_document": None
                }
            
            total_storage = sum(doc.get("file_size", 0) for doc in documents.data)
            created_dates = [doc["created_at"] for doc in documents.data if doc.get("created_at")]
            
            return {
                "total_documents": len(documents.data),
                "total_storage_bytes": total_storage,
                "total_storage_mb": round(total_storage / (1024 * 1024), 2),
                "oldest_document": min(created_dates) if created_dates else None,
                "newest_document": max(created_dates) if created_dates else None
            }
            
        except Exception as e:
            logger.error(f"Error getting storage stats for user {user_id}: {e}")
            return {"error": str(e)}


# Convenience functions
def cleanup_user_storage(user_id: str, tier: str) -> Dict[str, int]:
    """Clean up storage for a specific user"""
    return StorageCleanupService.cleanup_user_data(user_id, tier)


def cleanup_all_storage() -> Dict[str, any]:
    """Clean up storage for all users"""
    return StorageCleanupService.cleanup_all_users()


def cleanup_anonymous_storage() -> Dict[str, int]:
    """Clean up anonymous uploads"""
    return StorageCleanupService.cleanup_anonymous_uploads()


def get_user_storage_stats(user_id: str) -> Dict[str, any]:
    """Get storage statistics for a user"""
    return StorageCleanupService.get_storage_stats(user_id)


# CLI interface for manual cleanup
if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("🧹 STORAGE CLEANUP SERVICE")
    print("="*60 + "\n")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "cleanup-all":
            print("Cleaning up storage for all users...")
            result = cleanup_all_storage()
            print(f"\n✅ Results:")
            print(f"   Users cleaned: {result.get('users_cleaned', 0)}")
            print(f"   Documents deleted: {result.get('total_documents_deleted', 0)}")
            print(f"   Invoices deleted: {result.get('total_invoices_deleted', 0)}")
            
        elif command == "cleanup-anonymous":
            print("Cleaning up anonymous uploads...")
            result = cleanup_anonymous_storage()
            print(f"\n✅ Results:")
            print(f"   Documents deleted: {result.get('documents_deleted', 0)}")
            print(f"   Invoices deleted: {result.get('invoices_deleted', 0)}")
            
        elif command == "stats":
            if len(sys.argv) > 2:
                user_id = sys.argv[2]
                print(f"Getting storage stats for user: {user_id}")
                stats = get_user_storage_stats(user_id)
                print(f"\n📊 Storage Stats:")
                print(f"   Documents: {stats.get('total_documents', 0)}")
                print(f"   Storage: {stats.get('total_storage_mb', 0)} MB")
            else:
                print("❌ Please provide user_id: python storage_cleanup.py stats <user_id>")
        else:
            print(f"❌ Unknown command: {command}")
            print("\nAvailable commands:")
            print("  cleanup-all       - Clean up storage for all users")
            print("  cleanup-anonymous - Clean up anonymous uploads")
            print("  stats <user_id>   - Get storage stats for a user")
    else:
        print("Available commands:")
        print("  cleanup-all       - Clean up storage for all users")
        print("  cleanup-anonymous - Clean up anonymous uploads")
        print("  stats <user_id>   - Get storage stats for a user")
        print("\nUsage: python storage_cleanup.py <command>")
    
    print("\n" + "="*60 + "\n")
