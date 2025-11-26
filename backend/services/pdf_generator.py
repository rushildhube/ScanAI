from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from datetime import datetime
import os
from typing import Dict, List, Any

class PDFGenerator:
    """
    Enhanced PDF generator for dental health analysis reports with professional medical formatting.
    """
    
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Color scheme for medical reports
        self.colors = {
            'primary': HexColor('#2563eb'),
            'secondary': HexColor('#16a34a'),
            'warning': HexColor('#f59e0b'),
            'danger': HexColor('#dc2626'),
            'light_gray': HexColor('#f8fafc'),
            'dark_gray': HexColor('#374151'),
            'text_primary': HexColor('#1e293b'),
            'text_secondary': HexColor('#64748b')
        }

    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the medical report."""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#1e293b'),
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=12,
            textColor=HexColor('#2563eb'),
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=HexColor('#e5e7eb'),
            borderPadding=8,
            backColor=HexColor('#f8fafc')
        ))
        
        # Diagnosis style
        self.styles.add(ParagraphStyle(
            name='Diagnosis',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            textColor=HexColor('#1e293b'),
            fontName='Helvetica-Bold'
        ))
        
        # Confidence style
        self.styles.add(ParagraphStyle(
            name='Confidence',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=HexColor('#16a34a'),
            fontName='Helvetica'
        ))

    def generate_report(self, user_data, analysis_results):
        """Generate a comprehensive dental health analysis report."""
        doc = SimpleDocTemplate(
            self.output_path, 
            pagesize=A4,
            rightMargin=2*cm, 
            leftMargin=2*cm,
            topMargin=2*cm, 
            bottomMargin=2*cm
        )
        story = []

        # Header with logo and title
        story.extend(self._create_header())
        
        # Patient information section
        story.extend(self._create_patient_info_section(user_data))
        
        # AI diagnosis section
        story.extend(self._create_diagnosis_section(analysis_results))
        
        # Image analysis results
        story.extend(self._create_image_analysis_section(analysis_results))
        
        # Detailed recommendations
        story.extend(self._create_recommendations_section(analysis_results))
        
        # Technical information
        story.extend(self._create_technical_section(analysis_results))
        
        # Footer and disclaimer
        story.extend(self._create_footer())

        # Build the PDF
        doc.build(story)

    def _create_header(self):
        """Create the report header with logo and title."""
        elements = []
        
        # Main title
        elements.append(Paragraph("🦷 DENTAL HEALTH ANALYSIS REPORT", self.styles['ReportTitle']))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Subtitle
        elements.append(Paragraph("AI-Powered Dental Disease Classification System", self.styles['Normal']))
        elements.append(Paragraph("Model Accuracy: 92.28% | Vision Transformer (ViT-B/16)", self.styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Report generation info
        current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        elements.append(Paragraph(f"Report Generated: {current_time}", self.styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements

    def _create_patient_info_section(self, user_data):
        """Create patient information section."""
        elements = []
        
        elements.append(Paragraph("PATIENT INFORMATION", self.styles['SectionHeader']))
        
        # Create patient info table
        patient_data = [
            ['Name:', user_data.get('name', 'N/A')],
            ['Age:', str(user_data.get('age', 'N/A'))],
            ['Email:', user_data.get('email', 'N/A')],
            ['Phone:', user_data.get('mobile', 'N/A')],
            ['Location:', f"{user_data.get('city', 'N/A')}, {user_data.get('state', 'N/A')}"],
            ['Gender:', user_data.get('sex', 'N/A')]
        ]
        
        patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e5e7eb'))
        ]))
        
        elements.append(patient_table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements

    def _create_diagnosis_section(self, analysis_results):
        """Create AI diagnosis section with confidence analysis."""
        elements = []
        
        elements.append(Paragraph("AI DIAGNOSIS & ANALYSIS", self.styles['SectionHeader']))
        
        # Primary finding
        primary = analysis_results.get('primary_finding', {})
        primary_class = primary.get('class', 'Unknown')
        primary_confidence = primary.get('confidence', 0)
        
        elements.append(Paragraph(f"<b>Primary Finding:</b> {primary_class}", self.styles['Diagnosis']))
        elements.append(Paragraph(f"<b>Confidence Level:</b> {primary_confidence:.1%}", self.styles['Confidence']))
        
        # Additional findings
        additional = analysis_results.get('additional_findings', [])
        if additional:
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph("<b>Additional Findings:</b>", self.styles['Diagnosis']))
            for finding in additional:
                elements.append(Paragraph(f"• {finding.get('class', 'Unknown')} ({finding.get('confidence', 0):.1%})", 
                                         self.styles['Normal']))
        
        elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _create_image_analysis_section(self, analysis_results):
        """Create image analysis results section."""
        elements = []
        
        elements.append(Paragraph("IMAGE ANALYSIS RESULTS", self.styles['SectionHeader']))
        
        image_results = analysis_results.get('image_results', [])
        if image_results:
            elements.append(Paragraph(f"<b>Total Images Analyzed:</b> {len(image_results)}", self.styles['Diagnosis']))
            elements.append(Spacer(1, 0.1 * inch))
            
            for i, result in enumerate(image_results, 1):
                finding = result.get('finding', 'Unknown')
                elements.append(Paragraph(f"• Image {i}: {finding}", self.styles['Normal']))
        else:
            elements.append(Paragraph("No image analysis data available.", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _create_recommendations_section(self, analysis_results):
        """Create detailed recommendations section."""
        elements = []
        
        elements.append(Paragraph("RECOMMENDATIONS & NEXT STEPS", self.styles['SectionHeader']))
        
        primary = analysis_results.get('primary_finding', {})
        primary_class = primary.get('class', 'Unknown')
        
        # Get specific recommendations
        recommendations = self._get_detailed_recommendations(primary_class)
        
        elements.append(Paragraph("<b>Immediate Actions:</b>", self.styles['Diagnosis']))
        for rec in recommendations['immediate']:
            elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(Paragraph("<b>Long-term Care:</b>", self.styles['Diagnosis']))
        for rec in recommendations['long_term']:
            elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(Paragraph("<b>When to See a Dentist:</b>", self.styles['Diagnosis']))
        for rec in recommendations['dental_visit']:
            elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _create_technical_section(self, analysis_results):
        """Create technical information section."""
        elements = []
        
        elements.append(Paragraph("TECHNICAL INFORMATION", self.styles['SectionHeader']))
        
        technical_data = [
            ['AI Model:', 'Vision Transformer (ViT-B/16)'],
            ['Model Accuracy:', '92.28%'],
            ['Training Data:', '6,000+ dental images'],
            ['Disease Classes:', '6 (Calculus, Caries, Gingivitis, Healthy Teeth, Mouth Ulcer, Tooth Discoloration)'],
            ['Image Processing:', '224x224 RGB normalization'],
            ['Confidence Threshold:', 'Dynamic based on primary prediction']
        ]
        
        tech_table = Table(technical_data, colWidths=[2*inch, 4*inch])
        tech_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e5e7eb'))
        ]))
        
        elements.append(tech_table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements

    def _create_footer(self):
        """Create footer with disclaimer."""
        elements = []
        
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("=" * 80, self.styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))
        
        disclaimer_text = """
        <b>IMPORTANT DISCLAIMER:</b><br/><br/>

        This report is generated by an AI system and not by a professional doctor. It is for educational and informational purposes only, under the doctrine of self-determination and/or information.
        It is NOT a substitute for professional dental diagnosis, treatment, or medical advice. The AI model has been trained on a dataset of dental images and is not 100% accurate. It is best to consult and receive care from a qualified dental professional for proper diagnosis and a 100% accurate treatment plan.
        The developers and providers of this AI system hold no responsibility for decisions regarding self-diagnosis and self-treatment made based on this report, as this is only for self-informative probabilities and/or non-professional educational purposes under the clause of the doctrine of self-determination and/or self-probable information for educational purposes.
        """

        elements.append(Paragraph(disclaimer_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(Paragraph("© 2024 Dental AI Classification System | Generated by AI", self.styles['Normal']))
        
        return elements

    def _get_detailed_recommendations(self, condition):
        """Get detailed recommendations based on the condition."""
        recommendations = {
            'Calculus': {
                'immediate': [
                    'Schedule a professional dental cleaning (scaling and root planing)',
                    'Increase frequency of brushing to twice daily with fluoride toothpaste',
                    'Use dental floss or interdental brushes daily',
                    'Consider using an antimicrobial mouthwash'
                ],
                'long_term': [
                    'Maintain regular dental checkups every 6 months',
                    'Follow a consistent oral hygiene routine',
                    'Consider professional cleaning every 3-4 months if prone to calculus buildup',
                    'Quit smoking if applicable, as it increases calculus formation'
                ],
                'dental_visit': [
                    'Within 1-2 weeks for professional cleaning',
                    'If experiencing bleeding gums or pain',
                    'If calculus buildup is visible or causing discomfort'
                ]
            },
            'Caries': {
                'immediate': [
                    'Schedule a dental appointment as soon as possible',
                    'Avoid sugary foods and drinks',
                    'Use fluoride toothpaste and mouthwash',
                    'Apply dental sealants if recommended by dentist'
                ],
                'long_term': [
                    'Maintain excellent oral hygiene with regular brushing and flossing',
                    'Limit sugar intake and acidic foods',
                    'Use fluoride treatments as recommended',
                    'Consider dental sealants for prevention'
                ],
                'dental_visit': [
                    'Within 1 week for cavity assessment and treatment',
                    'If experiencing tooth pain or sensitivity',
                    'For regular checkups every 6 months'
                ]
            },
            'Gingivitis': {
                'immediate': [
                    'Improve daily oral hygiene routine',
                    'Brush teeth twice daily with soft-bristled toothbrush',
                    'Floss daily to remove plaque between teeth',
                    'Use antimicrobial mouthwash'
                ],
                'long_term': [
                    'Maintain consistent oral hygiene practices',
                    'Schedule regular dental cleanings every 6 months',
                    'Consider professional deep cleaning if needed',
                    'Monitor gum health regularly'
                ],
                'dental_visit': [
                    'Within 2-3 weeks for professional cleaning',
                    'If gums are bleeding, swollen, or painful',
                    'For regular periodontal maintenance'
                ]
            },
            'Healthy Teeth': {
                'immediate': [
                    'Continue current oral hygiene routine',
                    'Maintain regular dental checkups',
                    'Keep up with preventive care'
                ],
                'long_term': [
                    'Continue excellent oral hygiene practices',
                    'Schedule regular dental checkups every 6 months',
                    'Consider preventive treatments like sealants',
                    'Maintain a balanced diet low in sugar'
                ],
                'dental_visit': [
                    'Continue regular 6-month checkups',
                    'If any changes in oral health occur',
                    'For routine preventive care'
                ]
            },
            'Mouth Ulcer': {
                'immediate': [
                    'Avoid spicy, acidic, or hot foods',
                    'Use over-the-counter oral pain relief if needed',
                    'Maintain gentle oral hygiene',
                    'Apply ice or cold compress to reduce pain'
                ],
                'long_term': [
                    'Identify and avoid triggers (stress, certain foods)',
                    'Maintain good oral hygiene',
                    'Consider stress management techniques',
                    'Ensure adequate nutrition and vitamin B12'
                ],
                'dental_visit': [
                    'If ulcer persists for more than 2 weeks',
                    'If ulcer is very large or painful',
                    'If multiple ulcers appear',
                    'If accompanied by fever or other symptoms'
                ]
            },
            'Tooth Discoloration': {
                'immediate': [
                    'Maintain good oral hygiene',
                    'Avoid staining foods and drinks (coffee, tea, wine)',
                    'Consider professional whitening consultation',
                    'Use whitening toothpaste if appropriate'
                ],
                'long_term': [
                    'Limit consumption of staining substances',
                    'Maintain regular dental cleanings',
                    'Consider professional whitening treatments',
                    'Protect teeth from trauma'
                ],
                'dental_visit': [
                    'For professional whitening consultation',
                    'If discoloration is sudden or severe',
                    'For regular cosmetic dental care',
                    'If discoloration affects multiple teeth'
                ]
            }
        }
        
        return recommendations.get(condition, {
            'immediate': ['Consult with a dental professional for proper diagnosis and treatment'],
            'long_term': ['Follow professional dental advice and maintain good oral hygiene'],
            'dental_visit': ['Schedule an appointment with a dentist for proper evaluation']
        })
