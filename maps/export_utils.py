"""
Export utilities for activity records to CSV and PDF formats
"""
import csv
import io
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Maximum records per export to prevent memory/timeout issues
MAX_EXPORT_RECORDS = 10000


def export_to_csv(queryset, fields, filename_prefix):
    """
    Export queryset to CSV format
    
    Args:
        queryset: Django queryset to export
        fields: List of field names to include
        filename_prefix: Prefix for the exported filename
    
    Returns:
        HttpResponse with CSV file
    """
    response = HttpResponse(content_type='text/csv')
    filename = f'{filename_prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    # Write header
    writer.writerow(fields)
    
    # Write data rows
    for obj in queryset:
        row = []
        for field in fields:
            value = obj
            for attr in field.split('__'):
                try:
                    value = getattr(value, attr)
                except AttributeError:
                    value = '-'
                    break
            # Handle callable methods
            if callable(value):
                value = value()
            row.append(str(value) if value is not None else '-')
        writer.writerow(row)
    
    return response


def export_assessments_to_csv(queryset, filter_info=None):
    """Export assessment records to CSV"""
    try:
        # Check record count
        total_count = queryset.count()
        if total_count > MAX_EXPORT_RECORDS:
            return JsonResponse({
                'error': f'Export limit exceeded. Maximum {MAX_EXPORT_RECORDS:,} records allowed. Found {total_count:,} records. Please apply filters to reduce the dataset.'
            }, status=400)
        
        if total_count == 0:
            return JsonResponse({
                'error': 'No records found to export. Please adjust your filters.'
            }, status=400)
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = f'assessments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Add metadata header
        writer.writerow(['# Flood Risk Assessment Records Export'])
        writer.writerow([f'# Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}'])
        writer.writerow([f'# Total Records: {total_count}'])
        if filter_info:
            for key, value in filter_info.items():
                writer.writerow([f'# {key}: {value}'])
        writer.writerow([])  # Empty row
        
        # Column headers
        writer.writerow(['#', 'Barangay', 'Staff Member', 'Username', 'Latitude', 'Longitude', 'Risk Code', 'Description', 'Date'])
        
        # Data rows with row numbers
        for idx, obj in enumerate(queryset, 1):
            writer.writerow([
                idx,
                obj.barangay,
                obj.user.get_full_name(),
                obj.user.username,
                f'{obj.latitude:.6f}',
                f'{obj.longitude:.6f}',
                obj.flood_risk_code,
                obj.flood_risk_description,
                obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to generate CSV export: {str(e)}'
        }, status=500)


def export_reports_to_csv(queryset, filter_info=None):
    """Export report records to CSV"""
    try:
        # Check record count
        total_count = queryset.count()
        if total_count > MAX_EXPORT_RECORDS:
            return JsonResponse({
                'error': f'Export limit exceeded. Maximum {MAX_EXPORT_RECORDS:,} records allowed. Found {total_count:,} records. Please apply filters to reduce the dataset.'
            }, status=400)
        
        if total_count == 0:
            return JsonResponse({
                'error': 'No records found to export. Please adjust your filters.'
            }, status=400)
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = f'reports_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Add metadata header
        writer.writerow(['# Flood Risk Reports Export'])
        writer.writerow([f'# Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}'])
        writer.writerow([f'# Total Records: {total_count}'])
        if filter_info:
            for key, value in filter_info.items():
                writer.writerow([f'# {key}: {value}'])
        writer.writerow([])  # Empty row
        
        # Column headers
        writer.writerow(['#', 'Barangay', 'Staff Member', 'Username', 'Latitude', 'Longitude', 'Risk Code', 'Risk Label', 'Date'])
        
        # Data rows with row numbers
        for idx, obj in enumerate(queryset, 1):
            writer.writerow([
                idx,
                obj.barangay,
                obj.user.get_full_name(),
                obj.user.username,
                f'{obj.latitude:.6f}',
                f'{obj.longitude:.6f}',
                obj.flood_risk_code,
                obj.flood_risk_label,
                obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to generate CSV export: {str(e)}'
        }, status=500)


def export_certificates_to_csv(queryset, filter_info=None):
    """Export certificate records to CSV"""
    try:
        # Check record count
        total_count = queryset.count()
        if total_count > MAX_EXPORT_RECORDS:
            return JsonResponse({
                'error': f'Export limit exceeded. Maximum {MAX_EXPORT_RECORDS:,} records allowed. Found {total_count:,} records. Please apply filters to reduce the dataset.'
            }, status=400)
        
        if total_count == 0:
            return JsonResponse({
                'error': 'No records found to export. Please adjust your filters.'
            }, status=400)
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = f'certificates_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Add metadata header
        writer.writerow(['# Flood Risk Certificates Export'])
        writer.writerow([f'# Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}'])
        writer.writerow([f'# Total Records: {total_count}'])
        if filter_info:
            for key, value in filter_info.items():
                writer.writerow([f'# {key}: {value}'])
        writer.writerow([])  # Empty row
        
        # Column headers
        writer.writerow(['#', 'Establishment', 'Owner', 'Location', 'Barangay', 'Staff Member', 'Latitude', 'Longitude', 'Susceptibility', 'Zone Status', 'Date'])
        
        # Data rows with row numbers
        for idx, obj in enumerate(queryset, 1):
            writer.writerow([
                idx,
                obj.establishment_name,
                obj.owner_name,
                obj.location,
                obj.barangay,
                obj.user.get_full_name(),
                f'{obj.latitude:.6f}',
                f'{obj.longitude:.6f}',
                obj.flood_susceptibility,
                obj.zone_status,
                obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to generate CSV export: {str(e)}'
        }, status=500)


def export_flood_activities_to_csv(queryset, filter_info=None):
    """Export flood record activities to CSV"""
    try:
        # Check record count
        total_count = queryset.count()
        if total_count > MAX_EXPORT_RECORDS:
            return JsonResponse({
                'error': f'Export limit exceeded. Maximum {MAX_EXPORT_RECORDS:,} records allowed. Found {total_count:,} records. Please apply filters to reduce the dataset.'
            }, status=400)
        
        if total_count == 0:
            return JsonResponse({
                'error': 'No records found to export. Please adjust your filters.'
            }, status=400)
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = f'flood_activities_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Add metadata header
        writer.writerow(['# Flood Activity Records Export'])
        writer.writerow([f'# Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}'])
        writer.writerow([f'# Total Records: {total_count}'])
        if filter_info:
            for key, value in filter_info.items():
                writer.writerow([f'# {key}: {value}'])
        writer.writerow([])  # Empty row
        
        # Column headers
        writer.writerow(['#', 'Event Type', 'Action', 'Staff Member', 'Event Date', 'Affected Barangays', 'Total Casualties', 'Dead', 'Injured', 'Missing', 'Affected Persons', 'Affected Families', 'Damage (PHP)', 'Date'])
        
        # Data rows with row numbers
        for idx, obj in enumerate(queryset, 1):
            writer.writerow([
                idx,
                obj.event_type,
                obj.action,
                obj.user.get_full_name(),
                obj.event_date.strftime('%Y-%m-%d %H:%M:%S'),
                obj.affected_barangays,
                obj.total_casualties,
                obj.casualties_dead,
                obj.casualties_injured,
                obj.casualties_missing,
                obj.affected_persons,
                obj.affected_families,
                f'{obj.damage_total_php:,.2f}',
                obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to generate CSV export: {str(e)}'
        }, status=500)


def export_user_logs_to_csv(queryset, filter_info=None):
    """Export user logs to CSV"""
    try:
        # Check record count
        total_count = queryset.count()
        if total_count > MAX_EXPORT_RECORDS:
            return JsonResponse({
                'error': f'Export limit exceeded. Maximum {MAX_EXPORT_RECORDS:,} records allowed. Found {total_count:,} records. Please apply filters to reduce the dataset.'
            }, status=400)
        
        if total_count == 0:
            return JsonResponse({
                'error': 'No records found to export. Please adjust your filters.'
            }, status=400)
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = f'user_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Add metadata header
        writer.writerow(['# User Activity Logs Export'])
        writer.writerow([f'# Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}'])
        writer.writerow([f'# Total Records: {total_count}'])
        if filter_info:
            for key, value in filter_info.items():
                writer.writerow([f'# {key}: {value}'])
        writer.writerow([])  # Empty row
        
        # Column headers
        writer.writerow(['#', 'Action', 'Staff Member', 'Username', 'Position', 'Timestamp'])
        
        # Data rows with row numbers
        for idx, obj in enumerate(queryset, 1):
            # Get position display value
            if obj.user.position == 'others' and obj.user.custom_position:
                position_display = obj.user.custom_position
            else:
                position_display = obj.user.get_position_display() if hasattr(obj.user, 'get_position_display') else obj.user.position
            
            writer.writerow([
                idx,
                obj.action,
                obj.user.get_full_name(),
                obj.user.username,
                position_display or 'Not specified',
                obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to generate CSV export: {str(e)}'
        }, status=500)


def export_to_pdf(title, headers, data, filename_prefix, filter_info=None, summary_stats=None):
    """
    Export data to PDF format with modern, clean design
    
    Args:
        title: PDF title
        headers: List of column headers
        data: List of lists containing row data
        filename_prefix: Prefix for the exported filename
        filter_info: Dictionary of applied filters
        summary_stats: Dictionary of summary statistics
    
    Returns:
        HttpResponse with PDF file or JsonResponse with error
    """
    try:
        # Check record count
        total_count = len(data)
        if total_count > MAX_EXPORT_RECORDS:
            return JsonResponse({
                'error': f'Export limit exceeded. Maximum {MAX_EXPORT_RECORDS:,} records allowed. Found {total_count:,} records. Please apply filters to reduce the dataset.'
            }, status=400)
        
        if total_count == 0:
            return JsonResponse({
                'error': 'No records found to export. Please adjust your filters.'
            }, status=400)
    
        response = HttpResponse(content_type='application/pdf')
        filename = f'{filename_prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Create PDF with custom margins - wider for better table spacing
        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(letter),
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            leftMargin=0.4*inch,
            rightMargin=0.4*inch
        )
        elements = []
        
        # Modern color scheme
        primary_color = colors.HexColor('#256BE4')
        secondary_color = colors.HexColor('#1E3A5F')
        light_bg = colors.HexColor('#F8FAFC')
        border_color = colors.HexColor('#E2E8F0')
        text_dark = colors.HexColor('#1A202C')
        
        # Title style - modern and clean
        title_style = ParagraphStyle(
            'ModernTitle',
            parent=getSampleStyleSheet()['Heading1'],
            fontSize=18,
            textColor=primary_color,
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Subtitle style
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=12,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        # Add header section
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(f'Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}', subtitle_style))
        
        # Add summary statistics
        if summary_stats:
            summary_text = f"Total Records: {summary_stats.get('total', len(data))}" 
            if 'filtered' in summary_stats and summary_stats['filtered']:
                summary_text += " (Filtered)"
            elements.append(Paragraph(summary_text, subtitle_style))
        
        # Add filter information
        if filter_info:
            filter_text = ' | '.join([f"{k}: {v}" for k, v in filter_info.items()])
            filter_style = ParagraphStyle(
                'FilterInfo',
                parent=getSampleStyleSheet()['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#475569'),
                spaceAfter=12,
                alignment=TA_LEFT,
                fontName='Helvetica-Oblique'
            )
            elements.append(Paragraph(f"Filters Applied: {filter_text}", filter_style))
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Add row numbers to data
        numbered_data = [[idx] + row for idx, row in enumerate(data, 1)]
        
        # Prepare table data with headers (add # column)
        table_headers = ['#'] + headers
        table_data = [table_headers] + numbered_data
        
        # Dynamic column widths based on content type
        # Landscape letter: 11" width - 0.8" margins = 10.2" available
        available_width = 10.2 * inch
        
        # Allocate widths: row number column gets 0.4", distribute rest
        row_num_width = 0.4 * inch
        remaining_width = available_width - row_num_width
        
        # Smart column width allocation (can be customized per export type)
        num_cols = len(headers)
        col_widths = [row_num_width] + [remaining_width / num_cols] * num_cols
        
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Modern table styling with better text wrapping
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, 0), 10),
            
            # Body styling - alternating rows with better spacing
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
            
            # Cell borders - subtle
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            
            # Text alignment and font with word wrapping
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TEXTCOLOR', (0, 1), (-1, -1), text_dark),
            ('ALIGNMENT', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 1), (-1, -1), 'CJK'),
        ]))
    
        elements.append(table)
        
        # Footer
        elements.append(Spacer(1, 0.2*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#94A3B8'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        elements.append(Paragraph('SCDRRMO - Flood Monitoring System with GIS', footer_style))
        
        # Build PDF
        doc.build(elements)
        return response
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to build PDF document: {str(e)}. The dataset may be too large or contain problematic characters.'
        }, status=500)


def prepare_assessments_data(queryset):
    """Prepare assessment data for PDF export"""
    headers = ['Barangay', 'Staff Member', 'Risk Code', 'Description', 'Coordinates', 'Date']
    data = []
    for obj in queryset:
        # Smart truncation with word boundaries
        desc = obj.flood_risk_description
        if len(desc) > 50:
            desc = desc[:47] + '...'
        
        data.append([
            obj.barangay,
            obj.user.get_full_name(),
            obj.flood_risk_code,
            desc,
            f'{obj.latitude:.4f}, {obj.longitude:.4f}',
            obj.timestamp.strftime('%b %d, %Y')
        ])
    return headers, data


def prepare_reports_data(queryset):
    """Prepare reports data for PDF export"""
    headers = ['Barangay', 'Staff Member', 'Risk Code', 'Risk Label', 'Coordinates', 'Date']
    data = []
    for obj in queryset:
        # Smart truncation with word boundaries
        label = obj.flood_risk_label
        if len(label) > 50:
            label = label[:47] + '...'
        
        data.append([
            obj.barangay,
            obj.user.get_full_name(),
            obj.flood_risk_code,
            label,
            f'{obj.latitude:.4f}, {obj.longitude:.4f}',
            obj.timestamp.strftime('%b %d, %Y')
        ])
    return headers, data


def prepare_certificates_data(queryset):
    """Prepare certificates data for PDF export"""
    headers = ['Establishment', 'Owner', 'Location', 'Barangay', 'Susceptibility', 'Zone Status', 'Date']
    data = []
    for obj in queryset:
        # Smart truncation
        est_name = obj.establishment_name
        if len(est_name) > 30:
            est_name = est_name[:27] + '...'
        
        owner = obj.owner_name
        if len(owner) > 25:
            owner = owner[:22] + '...'
        
        loc = obj.location
        if len(loc) > 25:
            loc = loc[:22] + '...'
        
        data.append([
            est_name,
            owner,
            loc,
            obj.barangay,
            obj.flood_susceptibility[:25],
            obj.zone_status[:25],
            obj.timestamp.strftime('%b %d, %Y')
        ])
    return headers, data


def prepare_flood_activities_data(queryset):
    """Prepare flood activities data for PDF export"""
    headers = ['Event Type', 'Action', 'Staff Member', 'Affected Areas', 'Casualties', 'People', 'Damage (PHP)', 'Date']
    data = []
    for obj in queryset:
        # Smart truncation
        event = obj.event_type
        if len(event) > 25:
            event = event[:22] + '...'
        
        areas = obj.affected_barangays
        if len(areas) > 30:
            areas = areas[:27] + '...'
        
        data.append([
            event,
            obj.action,
            obj.user.get_full_name(),
            areas,
            f"{obj.total_casualties}",
            f"{obj.affected_persons} persons",
            f"₱{obj.damage_total_php:,.0f}",
            obj.timestamp.strftime('%b %d, %Y')
        ])
    return headers, data


def prepare_user_logs_data(queryset):
    """Prepare user logs data for PDF export"""
    headers = ['Action', 'Staff Member', 'Username', 'Position', 'Date & Time']
    data = []
    for obj in queryset:
        # Get position display value
        if obj.user.position == 'others' and obj.user.custom_position:
            position_display = obj.user.custom_position
        else:
            position_display = obj.user.get_position_display() if hasattr(obj.user, 'get_position_display') else obj.user.position
        
        # Smart truncation
        action = obj.action
        if len(action) > 30:
            action = action[:27] + '...'
        
        data.append([
            action,
            obj.user.get_full_name(),
            obj.user.username,
            position_display or 'Not specified',
            obj.timestamp.strftime('%b %d, %Y %I:%M %p')
        ])
    return headers, data
