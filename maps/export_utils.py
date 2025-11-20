"""
Export utilities for activity records to CSV and PDF formats
"""
import csv
import io
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


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


def export_assessments_to_csv(queryset):
    """Export assessment records to CSV"""
    response = HttpResponse(content_type='text/csv')
    filename = f'assessments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Barangay', 'Staff Member', 'Username', 'Latitude', 'Longitude', 'Risk Code', 'Description', 'Date'])
    
    for obj in queryset:
        writer.writerow([
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


def export_reports_to_csv(queryset):
    """Export report records to CSV"""
    response = HttpResponse(content_type='text/csv')
    filename = f'reports_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Barangay', 'Staff Member', 'Username', 'Latitude', 'Longitude', 'Risk Code', 'Risk Label', 'Date'])
    
    for obj in queryset:
        writer.writerow([
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


def export_certificates_to_csv(queryset):
    """Export certificate records to CSV"""
    response = HttpResponse(content_type='text/csv')
    filename = f'certificates_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Establishment', 'Owner', 'Location', 'Barangay', 'Staff Member', 'Latitude', 'Longitude', 'Susceptibility', 'Zone Status', 'Date'])
    
    for obj in queryset:
        writer.writerow([
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


def export_flood_activities_to_csv(queryset):
    """Export flood record activities to CSV"""
    response = HttpResponse(content_type='text/csv')
    filename = f'flood_activities_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Event Type', 'Action', 'Staff Member', 'Event Date', 'Affected Barangays', 'Total Casualties', 'Dead', 'Injured', 'Missing', 'Affected Persons', 'Affected Families', 'Damage (PHP)', 'Date'])
    
    for obj in queryset:
        writer.writerow([
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


def export_user_logs_to_csv(queryset):
    """Export user logs to CSV"""
    response = HttpResponse(content_type='text/csv')
    filename = f'user_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    # Write header
    writer.writerow(['Action', 'Staff Member', 'Username', 'Position', 'Timestamp'])
    
    # Write data rows
    for obj in queryset:
        # Get position display value
        if obj.user.position == 'others' and obj.user.custom_position:
            position_display = obj.user.custom_position
        else:
            position_display = obj.user.get_position_display() if hasattr(obj.user, 'get_position_display') else obj.user.position
        
        writer.writerow([
            obj.action,
            obj.user.get_full_name(),
            obj.user.username,
            position_display or 'Not specified',
            obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response


def export_to_pdf(title, headers, data, filename_prefix):
    """
    Export data to PDF format with modern, clean design
    
    Args:
        title: PDF title
        headers: List of column headers
        data: List of lists containing row data
        filename_prefix: Prefix for the exported filename
    
    Returns:
        HttpResponse with PDF file
    """
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
    elements.append(Spacer(1, 0.15*inch))
    
    # Prepare table data with headers
    table_data = [headers] + data
    
    # Create table with wider columns to prevent cramping
    # Calculate width to use available space on landscape page
    # Landscape letter: 11" width - 0.8" margins = 10.2" available
    col_widths = [10.2 * inch / len(headers)] * len(headers)
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


def prepare_assessments_data(queryset):
    """Prepare assessment data for PDF export"""
    headers = ['Barangay', 'Staff Member', 'Risk Code', 'Description', 'Coordinates', 'Date']
    data = []
    for obj in queryset:
        data.append([
            obj.barangay,
            obj.user.get_full_name(),
            obj.flood_risk_code,
            obj.flood_risk_description[:40] + ('...' if len(obj.flood_risk_description) > 40 else ''),
            f'{obj.latitude:.4f}, {obj.longitude:.4f}',
            obj.timestamp.strftime('%b %d, %Y')
        ])
    return headers, data


def prepare_reports_data(queryset):
    """Prepare reports data for PDF export"""
    headers = ['Barangay', 'Staff Member', 'Risk Code', 'Risk Label', 'Coordinates', 'Date']
    data = []
    for obj in queryset:
        data.append([
            obj.barangay,
            obj.user.get_full_name(),
            obj.flood_risk_code,
            obj.flood_risk_label[:40] + ('...' if len(obj.flood_risk_label) > 40 else ''),
            f'{obj.latitude:.4f}, {obj.longitude:.4f}',
            obj.timestamp.strftime('%b %d, %Y')
        ])
    return headers, data


def prepare_certificates_data(queryset):
    """Prepare certificates data for PDF export"""
    headers = ['Establishment', 'Owner', 'Location', 'Barangay', 'Susceptibility', 'Zone Status', 'Date']
    data = []
    for obj in queryset:
        data.append([
            obj.establishment_name[:25] + ('...' if len(obj.establishment_name) > 25 else ''),
            obj.owner_name[:20] + ('...' if len(obj.owner_name) > 20 else ''),
            obj.location[:20] + ('...' if len(obj.location) > 20 else ''),
            obj.barangay,
            obj.flood_susceptibility[:20],
            obj.zone_status[:20],
            obj.timestamp.strftime('%b %d, %Y')
        ])
    return headers, data


def prepare_flood_activities_data(queryset):
    """Prepare flood activities data for PDF export"""
    headers = ['Event Type', 'Action', 'Staff Member', 'Affected Areas', 'Casualties', 'People', 'Damage (PHP)', 'Date']
    data = []
    for obj in queryset:
        data.append([
            obj.event_type[:20],
            obj.action,
            obj.user.get_full_name(),
            obj.affected_barangays[:25] + ('...' if len(obj.affected_barangays) > 25 else ''),
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
        
        data.append([
            obj.action[:25],
            obj.user.get_full_name(),
            obj.user.username,
            position_display or 'Not specified',
            obj.timestamp.strftime('%b %d, %Y %I:%M %p')
        ])
    return headers, data
