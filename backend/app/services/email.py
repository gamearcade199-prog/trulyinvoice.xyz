"""
Email Service
FIX #12: Email Notifications System

Handles account verification, password reset, subscription notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict
from app.core.config import settings
import logging
from jinja2 import Template

logger = logging.getLogger(__name__)


class EmailService:
    """Send emails for various events"""
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        Send email
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text fallback
            reply_to: Reply-to address
        
        Returns:
            True if successful
        """
        try:
            if not settings.SMTP_HOST:
                logger.warning("⚠️  SMTP not configured - email not sent")
                return False
            
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.EMAIL_FROM
            msg["To"] = to_email
            
            if reply_to:
                msg["Reply-To"] = reply_to
            
            # Add plain text and HTML
            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            
            # Send
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"✅ Email sent to {to_email}: {subject}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_verification_email(user_email: str, verification_link: str) -> bool:
        """Send email verification link"""
        
        subject = "Verify your TrulyInvoice Account"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Welcome to TrulyInvoice!</h2>
                <p>Please verify your email address to activate your account.</p>
                <a href="{verification_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Verify Email
                </a>
                <p>Link expires in 24 hours.</p>
                <p>If you didn't create an account, please ignore this email.</p>
            </body>
        </html>
        """
        
        text_body = f"Verify your email: {verification_link}"
        
        return EmailService.send_email(user_email, subject, html_body, text_body)
    
    @staticmethod
    def send_password_reset_email(user_email: str, reset_link: str) -> bool:
        """Send password reset link"""
        
        subject = "Reset your TrulyInvoice Password"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Password Reset Request</h2>
                <p>We received a request to reset your password.</p>
                <a href="{reset_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Reset Password
                </a>
                <p>Link expires in 1 hour.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </body>
        </html>
        """
        
        text_body = f"Reset your password: {reset_link}"
        
        return EmailService.send_email(user_email, subject, html_body, text_body)
    
    @staticmethod
    def send_payment_confirmation(
        user_email: str,
        amount: float,
        tier: str,
        invoice_number: str
    ) -> bool:
        """Send payment confirmation"""
        
        subject = f"Payment Confirmation - Invoice #{invoice_number}"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Payment Received</h2>
                <p>Thank you for your payment!</p>
                <table style="border-collapse: collapse;">
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>Amount</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">₹{amount:,.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>Plan</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{tier.capitalize()}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>Invoice</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">#{invoice_number}</td>
                    </tr>
                </table>
                <p style="margin-top: 20px;">Your {tier} plan is now active. Start scanning invoices!</p>
            </body>
        </html>
        """
        
        text_body = f"Payment confirmed: ₹{amount} for {tier} plan"
        
        return EmailService.send_email(user_email, subject, html_body, text_body)
    
    @staticmethod
    def send_subscription_upgraded(user_email: str, new_tier: str) -> bool:
        """Send subscription upgrade confirmation"""
        
        subject = f"Welcome to {new_tier.capitalize()} Plan!"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Subscription Upgraded!</h2>
                <p>Your account has been upgraded to the <strong>{new_tier.capitalize()}</strong> plan.</p>
                <p>You now have access to:</p>
                <ul>
                    <li>Unlimited scans per month</li>
                    <li>Advanced analytics</li>
                    <li>Priority support</li>
                </ul>
                <p>Start using your new features now!</p>
            </body>
        </html>
        """
        
        return EmailService.send_email(user_email, subject, html_body)
    
    @staticmethod
    def send_subscription_renewal_reminder(
        user_email: str,
        renewal_date: str,
        tier: str
    ) -> bool:
        """Send subscription renewal reminder"""
        
        subject = "Your TrulyInvoice Plan Renews Soon"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Renewal Reminder</h2>
                <p>Your <strong>{tier.capitalize()}</strong> plan will renew on <strong>{renewal_date}</strong>.</p>
                <p>No action needed - your subscription will automatically renew.</p>
                <p>If you'd like to cancel or change your plan, please manage it in your account settings.</p>
            </body>
        </html>
        """
        
        return EmailService.send_email(user_email, subject, html_body)
    
    @staticmethod
    def send_invoice_processed(
        user_email: str,
        invoice_filename: str,
        confidence_score: float
    ) -> bool:
        """Send invoice processing completion notification"""
        
        subject = f"Invoice Processed: {invoice_filename}"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Invoice Processed Successfully</h2>
                <p>Your invoice has been processed.</p>
                <table style="border-collapse: collapse;">
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>File</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{invoice_filename}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><b>Confidence</b></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{confidence_score*100:.1f}%</td>
                    </tr>
                </table>
                <p style="margin-top: 20px;">View your extracted data in the dashboard.</p>
            </body>
        </html>
        """
        
        return EmailService.send_email(user_email, subject, html_body)
    
    @staticmethod
    def send_bulk_email(to_emails: List[str], subject: str, html_body: str) -> int:
        """Send email to multiple recipients"""
        
        success_count = 0
        for email in to_emails:
            if EmailService.send_email(email, subject, html_body):
                success_count += 1
        
        logger.info(f"📧 Sent {success_count}/{len(to_emails)} emails")
        return success_count


if __name__ == "__main__":
    print("✅ Email Service module loaded")
    print("\nAvailable email types:")
    print("  - Verification emails")
    print("  - Password reset")
    print("  - Payment confirmations")
    print("  - Subscription notifications")
    print("  - Processing updates")
