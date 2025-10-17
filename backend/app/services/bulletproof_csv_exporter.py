"""
🚀 BULLETPROOF 10/10 CSV EXPORTER - GEMINI COMPATIBLE
========================================================

Uses ALL data from our bulletproof Gemini extractor including:
- 50+ fields from bulletproof extractor
- Multiple CSV formats (summary, detailed, analytics)
- Complete field mapping for data analysis
- Export options for different use cases
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class BulletproofCSVExporter:
    """
    Creates comprehensive CSV exports using ALL data from bulletproof Gemini extractor
    """
    
    def __init__(self):
        # Define field mappings for different export types
        self.field_mappings = {
            'summary': [
                'invoice_number', 'invoice_date', 'vendor_name', 'vendor_gstin',
                'customer_name', 'total_amount', 'currency', 'payment_status',
                'cgst', 'sgst', 'igst', 'total_gst', 'created_at'
            ],
            'detailed': [
                # Core fields
                'invoice_number', 'invoice_date', 'due_date', 'vendor_name', 'vendor_gstin',
                'vendor_pan', 'vendor_email', 'vendor_phone', 'vendor_address', 'vendor_state',
                'vendor_pincode', 'customer_name', 'customer_gstin', 'customer_address',
                'customer_state', 'customer_phone',
                # Financial fields
                'total_amount', 'currency', 'subtotal', 'taxable_amount', 'discount',
                'shipping_charges', 'other_charges', 'roundoff',
                # Tax fields
                'cgst', 'sgst', 'igst', 'ugst', 'cess', 'total_gst', 'vat', 'service_tax',
                'tds_amount', 'tds_percentage', 'tcs_amount',
                # GST compliance
                'hsn_code', 'sac_code', 'place_of_supply', 'invoice_type', 'supply_type',
                'reverse_charge',
                # Banking
                'bank_name', 'account_number', 'ifsc_code', 'swift_code',
                # References
                'po_number', 'po_date', 'payment_method', 'payment_terms',
                # Status
                'payment_status', 'created_at', 'updated_at'
            ],
            'analytics': [
                # All fields for complete data analysis
                'invoice_number', 'invoice_date', 'due_date', 'vendor_name', 'vendor_gstin',
                'vendor_pan', 'vendor_tan', 'vendor_email', 'vendor_phone', 'vendor_address',
                'vendor_state', 'vendor_pincode', 'vendor_type', 'customer_name', 'customer_gstin',
                'customer_address', 'customer_state', 'customer_phone', 'total_amount', 'currency',
                'subtotal', 'taxable_amount', 'discount', 'discount_percentage', 'shipping_charges',
                'packing_charges', 'handling_charges', 'insurance_charges', 'other_charges',
                'roundoff', 'cgst', 'sgst', 'igst', 'ugst', 'cess', 'total_gst', 'vat',
                'service_tax', 'tds_amount', 'tds_percentage', 'tcs_amount', 'hsn_code',
                'sac_code', 'place_of_supply', 'invoice_type', 'supply_type', 'reverse_charge',
                'bank_name', 'account_number', 'ifsc_code', 'swift_code', 'po_number', 'po_date',
                'challan_number', 'eway_bill_number', 'lr_number', 'bill_of_entry',
                'bill_of_entry_date', 'port_code', 'payment_status', 'payment_method',
                'payment_terms', 'created_at', 'updated_at'
            ]
        }
    
    def export_invoice(self, invoice_data: Dict, export_type: str = 'detailed', filename: str = None) -> str:
        """
        Export single invoice to CSV format
        
        Args:
            invoice_data: Complete invoice data from bulletproof extractor
            export_type: 'summary', 'detailed', or 'analytics'
            filename: Optional custom filename
            
        Returns:
            Path to created CSV file
        """
        if not filename:
            invoice_num = invoice_data.get('invoice_number', 'INVOICE').replace('/', '_')
            vendor_name = invoice_data.get('vendor_name', 'VENDOR').replace(' ', '_')[:15]
            filename = f"Invoice_{export_type}_{invoice_num}_{vendor_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        
        # Get field mapping for export type\n        fields = self.field_mappings.get(export_type, self.field_mappings['detailed'])\n        \n        # Create CSV\n        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:\n            writer = csv.DictWriter(csvfile, fieldnames=fields)\n            writer.writeheader()\n            \n            # Prepare row data\n            row_data = self._prepare_row_data(invoice_data, fields)\n            writer.writerow(row_data)\n        \n        print(f\"✅ Bulletproof {export_type} CSV exported: {filename}\")\n        return filename\n    \n    def export_multiple_invoices(self, invoices_data: List[Dict], export_type: str = 'detailed', filename: str = None) -> str:\n        \"\"\"\n        Export multiple invoices to CSV format\n        \n        Args:\n            invoices_data: List of invoice data dictionaries\n            export_type: 'summary', 'detailed', or 'analytics'\n            filename: Optional custom filename\n            \n        Returns:\n            Path to created CSV file\n        \"\"\"\n        if not filename:\n            timestamp = datetime.now().strftime('%Y%m%d_%H%M')\n            filename = f\"Invoices_{export_type}_{len(invoices_data)}_records_{timestamp}.csv\"\n        \n        # Get field mapping for export type\n        fields = self.field_mappings.get(export_type, self.field_mappings['detailed'])\n        \n        # Create CSV\n        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:\n            writer = csv.DictWriter(csvfile, fieldnames=fields)\n            writer.writeheader()\n            \n            # Write all invoices\n            for invoice_data in invoices_data:\n                row_data = self._prepare_row_data(invoice_data, fields)\n                writer.writerow(row_data)\n        \n        print(f\"✅ Bulletproof {export_type} CSV exported: {filename} ({len(invoices_data)} invoices)\")\n        return filename\n    \n    def export_line_items(self, invoices_data: List[Dict], filename: str = None) -> str:\n        \"\"\"\n        Export line items from invoices to separate CSV for detailed analysis\n        \n        Args:\n            invoices_data: List of invoice data dictionaries\n            filename: Optional custom filename\n            \n        Returns:\n            Path to created CSV file\n        \"\"\"\n        if not filename:\n            timestamp = datetime.now().strftime('%Y%m%d_%H%M')\n            filename = f\"Line_Items_Export_{timestamp}.csv\"\n        \n        # Line items fields\n        line_item_fields = [\n            'invoice_number', 'invoice_date', 'vendor_name', 'vendor_gstin',\n            'item_sequence', 'description', 'hsn_sac', 'unit', 'quantity',\n            'rate', 'discount', 'amount', 'item_confidence', 'total_amount',\n            'currency', 'created_at'\n        ]\n        \n        # Create CSV\n        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:\n            writer = csv.DictWriter(csvfile, fieldnames=line_item_fields)\n            writer.writeheader()\n            \n            # Extract line items from all invoices\n            for invoice_data in invoices_data:\n                line_items = invoice_data.get('line_items', [])\n                if not line_items:\n                    continue\n                \n                # Common invoice data\n                common_data = {\n                    'invoice_number': invoice_data.get('invoice_number', ''),\n                    'invoice_date': invoice_data.get('invoice_date', ''),\n                    'vendor_name': invoice_data.get('vendor_name', ''),\n                    'vendor_gstin': invoice_data.get('vendor_gstin', ''),\n                    'total_amount': invoice_data.get('total_amount', 0),\n                    'currency': invoice_data.get('currency', 'INR'),\n                    'created_at': invoice_data.get('created_at', '')\n                }\n                \n                # Write each line item\n                for idx, item in enumerate(line_items, 1):\n                    row_data = common_data.copy()\n                    row_data.update({\n                        'item_sequence': idx,\n                        'description': item.get('description', ''),\n                        'hsn_sac': item.get('hsn_sac', item.get('hsn', '')),\n                        'unit': item.get('unit', 'Nos'),\n                        'quantity': item.get('quantity', 1),\n                        'rate': item.get('rate', 0),\n                        'discount': item.get('discount', 0),\n                        'amount': item.get('amount', 0),\n                        'item_confidence': item.get('confidence', 0.9)\n                    })\n                    writer.writerow(row_data)\n        \n        print(f\"✅ Line items CSV exported: {filename}\")\n        return filename\n    \n    def export_financial_summary(self, invoices_data: List[Dict], filename: str = None) -> str:\n        \"\"\"\n        Export financial summary and analytics CSV\n        \n        Args:\n            invoices_data: List of invoice data dictionaries\n            filename: Optional custom filename\n            \n        Returns:\n            Path to created CSV file\n        \"\"\"\n        if not filename:\n            timestamp = datetime.now().strftime('%Y%m%d_%H%M')\n            filename = f\"Financial_Summary_{timestamp}.csv\"\n        \n        # Financial summary fields\n        financial_fields = [\n            'invoice_number', 'invoice_date', 'vendor_name', 'vendor_gstin',\n            'customer_name', 'total_amount', 'currency',\n            # Amounts breakdown\n            'subtotal', 'taxable_amount', 'discount', 'shipping_charges',\n            'other_charges', 'roundoff',\n            # Tax breakdown\n            'cgst', 'sgst', 'igst', 'ugst', 'cess', 'total_gst',\n            'cgst_rate', 'sgst_rate', 'igst_rate',\n            'vat', 'service_tax', 'tds_amount', 'tds_percentage', 'tcs_amount',\n            # Calculated fields\n            'tax_percentage', 'effective_rate', 'net_amount',\n            # Status\n            'payment_status', 'due_date', 'days_to_due', 'created_at'\n        ]\n        \n        # Create CSV\n        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:\n            writer = csv.DictWriter(csvfile, fieldnames=financial_fields)\n            writer.writeheader()\n            \n            # Process each invoice with calculations\n            for invoice_data in invoices_data:\n                row_data = self._prepare_financial_row(invoice_data)\n                writer.writerow(row_data)\n        \n        print(f\"✅ Financial summary CSV exported: {filename}\")\n        return filename\n    \n    def _prepare_row_data(self, invoice_data: Dict, fields: List[str]) -> Dict[str, Any]:\n        \"\"\"Prepare row data for CSV export\"\"\"\n        row_data = {}\n        \n        for field in fields:\n            value = invoice_data.get(field, '')\n            \n            # Handle different data types\n            if value is None:\n                row_data[field] = ''\n            elif isinstance(value, bool):\n                row_data[field] = 'Yes' if value else 'No'\n            elif isinstance(value, (list, dict)):\n                # Convert complex types to JSON string\n                row_data[field] = json.dumps(value) if value else ''\n            elif isinstance(value, (int, float)):\n                # Keep numbers as is, but handle zero\n                row_data[field] = value if value != 0 else ''\n            else:\n                row_data[field] = str(value) if value else ''\n        \n        return row_data\n    \n    def _prepare_financial_row(self, invoice_data: Dict) -> Dict[str, Any]:\n        \"\"\"Prepare enhanced financial row with calculations\"\"\"\n        # Base data\n        row_data = {\n            'invoice_number': invoice_data.get('invoice_number', ''),\n            'invoice_date': invoice_data.get('invoice_date', ''),\n            'vendor_name': invoice_data.get('vendor_name', ''),\n            'vendor_gstin': invoice_data.get('vendor_gstin', ''),\n            'customer_name': invoice_data.get('customer_name', ''),\n            'total_amount': invoice_data.get('total_amount', 0),\n            'currency': invoice_data.get('currency', 'INR'),\n            'subtotal': invoice_data.get('subtotal', 0),\n            'taxable_amount': invoice_data.get('taxable_amount', 0),\n            'discount': invoice_data.get('discount', 0),\n            'shipping_charges': invoice_data.get('shipping_charges', 0),\n            'other_charges': invoice_data.get('other_charges', 0),\n            'roundoff': invoice_data.get('roundoff', 0),\n            'cgst': invoice_data.get('cgst', 0),\n            'sgst': invoice_data.get('sgst', 0),\n            'igst': invoice_data.get('igst', 0),\n            'ugst': invoice_data.get('ugst', 0),\n            'cess': invoice_data.get('cess', 0),\n            'total_gst': invoice_data.get('total_gst', 0),\n            'vat': invoice_data.get('vat', 0),\n            'service_tax': invoice_data.get('service_tax', 0),\n            'tds_amount': invoice_data.get('tds_amount', 0),\n            'tds_percentage': invoice_data.get('tds_percentage', 0),\n            'tcs_amount': invoice_data.get('tcs_amount', 0),\n            'payment_status': invoice_data.get('payment_status', 'unpaid'),\n            'due_date': invoice_data.get('due_date', ''),\n            'created_at': invoice_data.get('created_at', '')\n        }\n        \n        # Calculate additional fields\n        total_amount = float(invoice_data.get('total_amount', 0))\n        taxable_amount = float(invoice_data.get('taxable_amount', 0))\n        total_gst = float(invoice_data.get('total_gst', 0))\n        cgst = float(invoice_data.get('cgst', 0))\n        sgst = float(invoice_data.get('sgst', 0))\n        igst = float(invoice_data.get('igst', 0))\n        \n        # GST rates (assuming standard calculation)\n        if taxable_amount > 0:\n            if cgst > 0:\n                row_data['cgst_rate'] = f\"{(cgst / taxable_amount * 100):.2f}%\"\n            if sgst > 0:\n                row_data['sgst_rate'] = f\"{(sgst / taxable_amount * 100):.2f}%\"\n            if igst > 0:\n                row_data['igst_rate'] = f\"{(igst / taxable_amount * 100):.2f}%\"\n            \n            # Total tax percentage\n            if total_gst > 0:\n                row_data['tax_percentage'] = f\"{(total_gst / taxable_amount * 100):.2f}%\"\n            \n            # Effective rate\n            if total_amount > 0:\n                row_data['effective_rate'] = f\"{(total_gst / total_amount * 100):.2f}%\"\n        \n        # Net amount (total - taxes)\n        row_data['net_amount'] = total_amount - total_gst\n        \n        # Days to due date calculation\n        if invoice_data.get('due_date'):\n            try:\n                from datetime import datetime\n                due_date = datetime.strptime(invoice_data['due_date'], '%Y-%m-%d').date()\n                today = datetime.now().date()\n                days_diff = (due_date - today).days\n                row_data['days_to_due'] = days_diff\n            except:\n                row_data['days_to_due'] = ''\n        else:\n            row_data['days_to_due'] = ''\n        \n        return row_data\n    \n    def get_available_export_types(self) -> Dict[str, str]:\n        \"\"\"Get available export types and their descriptions\"\"\"\n        return {\n            'summary': 'Basic invoice summary with key fields (13 columns)',\n            'detailed': 'Comprehensive invoice data for analysis (40+ columns)',\n            'analytics': 'Complete dataset for advanced analytics (50+ columns)',\n            'line_items': 'Individual line items from all invoices',\n            'financial': 'Financial summary with calculated metrics'\n        }\n    \n    def get_field_list(self, export_type: str) -> List[str]:\n        \"\"\"Get list of fields for specific export type\"\"\"\n        return self.field_mappings.get(export_type, [])