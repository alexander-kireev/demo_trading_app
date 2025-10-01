
from app.portfolio.portfolio_model import Portfolio

from app.portfolio.portfolio_service import (
    get_portfolio
)

from app.user.user_service import (
    get_user
)

import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime


class NumberedCanvas(canvas.Canvas):
    """Custom canvas class to add page numbers 'Page X of Y'"""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        page_number_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(200*mm, 15*mm, page_number_text)



def generate_portfolio_statement(user_id, filename=None):
    """
    Generates a PDF statement for a user's portfolio.
    Limits 25 positions per page.
    Auto-generates a unique filename if not provided.
    Saves into app/static/pdfs/portfolio_statement
    """
    # Fetch portfolio and user
    user = get_user(user_id)
    portfolio = get_portfolio(user_id)

    # Define save path inside static/pdfs/portfolio_statement
    base_dir = os.path.join(os.path.dirname(__file__), "static", "pdfs", "portfolio_statement")
    os.makedirs(base_dir, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portfolio_statement_{user_id}_{timestamp}.pdf"

    filepath = os.path.join(base_dir, filename)

    # Styles
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []

    # Header
    header_text = f"""
    <b>Demo Trading App – Portfolio Statement</b><br/>
    Name: {user.first_name} {user.last_name}<br/>
    User ID: {user.id}<br/>
    Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    elements.append(Paragraph(header_text, normal_style))
    elements.append(Spacer(1, 12))

    # Summary
    summary_text = f"""
    <b>Cash Balance:</b> ${portfolio.cash_balance:,.2f}<br/>
    <b>Equities Value:</b> ${portfolio.positions_value:,.2f}<br/>
    <b>Total Portfolio Value:</b> ${portfolio.portfolio_value:,.2f}
    """
    elements.append(Paragraph(summary_text, normal_style))
    elements.append(Spacer(1, 20))

    if not portfolio.positions:
        elements.append(Paragraph("You currently hold no equities.", normal_style))
        doc.build(elements, canvasmaker=NumberedCanvas)
        return filepath

    table_header = ["#", "Symbol", "Company", "Avg Cost", "Current Price", "Shares", "Position Value"]

    positions = list(portfolio.positions.values())
    row_number = 1
    for i in range(0, len(positions), 25):
        chunk = positions[i:i+25]
        table_data = [table_header]

        for pos in chunk:
            row = [
                str(row_number),
                pos.symbol,
                pos.company_name,
                f"${pos.price_per_share:,.2f}",
                f"${pos.last_price_per_share:,.2f}",
                str(pos.number_of_shares),
                f"${pos.total_value:,.2f}"
            ]
            table_data.append(row)
            row_number += 1

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
        ]))

        elements.append(table)

        if i + 25 < len(positions):
            elements.append(PageBreak())

    doc.build(elements, canvasmaker=NumberedCanvas)
    return filepath






def generate_trade_statement(user_id, trades, filename=None):
    """
    Generates a PDF statement for a user's trade history.
    Limits 25 trades per page.
    Adds page numbers, datetime, and numbered rows.
    
    Args:
        user_id: int
        trades: list of Trade objects
        filename: optional custom filename
    Returns:
        str: full filepath of generated PDF
    """
    # Fetch user info
    user = get_user(user_id)

    # Define save path inside static/pdfs/trade_history
    base_dir = os.path.join(os.path.dirname(__file__), "static", "pdfs", "trade_history")
    os.makedirs(base_dir, exist_ok=True)   # create folder if not exists

    # Unique filename if none provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"trade_history_{user_id}_{timestamp}.pdf"

    filepath = os.path.join(base_dir, filename)

    # Styles
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    # Document
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []

    # Header info
    header_text = f"""
    <b>Demo Trading App – Trade History</b><br/>
    Name: {user.first_name} {user.last_name}<br/>
    User ID: {user.id}<br/>
    Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    elements.append(Paragraph(header_text, normal_style))
    elements.append(Spacer(1, 12))

    # If no trades
    if not trades:
        elements.append(Paragraph("No trades found for the selected period.", normal_style))
        doc.build(elements, canvasmaker=NumberedCanvas)
        return filepath

    # Table header
    table_header = ["#", "Trade ID", "Date/Time", "Symbol", "Company", "Type", "Price/Share", "Shares", "Total Value"]

    # Split trades into chunks of 25
    row_number = 1
    for i in range(0, len(trades), 25):
        chunk = trades[i:i+25]

        # Build table rows
        table_data = [table_header]
        for trade in chunk:
            row = [
                str(row_number),
                getattr(trade, "trade_id", "-"),
                getattr(trade, "timestamp", "").strftime("%Y-%m-%d %H:%M:%S") if getattr(trade, "timestamp", None) else "-",
                trade.symbol,
                trade.company_name,
                trade.trade_type.upper(),
                f"${trade.price_per_share:,.2f}",
                str(trade.number_of_shares),
                f"${trade.trade_total:,.2f}"
            ]
            table_data.append(row)
            row_number += 1

        # Create table
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
        ]))

        elements.append(table)

        # Add page break if not last chunk
        if i + 25 < len(trades):
            elements.append(PageBreak())

    # Build PDF with custom canvas (adds page numbers)
    doc.build(elements, canvasmaker=NumberedCanvas)
    return filepath










def generate_transaction_statement(user_id, transactions, filename=None):
    """
    Generates a PDF statement for a user's transaction history.
    Limits 25 transactions per page.
    Adds page numbers, datetime, and numbered rows.
    
    Args:
        user_id: int
        transactions: list of Transaction objects
        filename: optional custom filename
    Returns:
        str: full filepath of generated PDF
    """
    # Fetch user info
    user = get_user(user_id)

    # Define save path inside static/pdfs/transaction_history
    base_dir = os.path.join(os.path.dirname(__file__), "static", "pdfs", "transaction_history")
    os.makedirs(base_dir, exist_ok=True)

    # Unique filename if none provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transaction_history_{user_id}_{timestamp}.pdf"

    filepath = os.path.join(base_dir, filename)

    # Styles
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []

    # Header info
    header_text = f"""
    <b>Demo Trading App – Transaction History</b><br/>
    Name: {user.first_name} {user.last_name}<br/>
    User ID: {user.id}<br/>
    Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    elements.append(Paragraph(header_text, normal_style))
    elements.append(Spacer(1, 12))

    # If no transactions
    if not transactions:
        elements.append(Paragraph("No transactions found for the selected period.", normal_style))
        doc.build(elements, canvasmaker=NumberedCanvas)
        return filepath

    # Table header
    table_header = ["#", "Transaction ID", "Date/Time", "Type", "Amount"]

    # Split into chunks of 25
    row_number = 1
    for i in range(0, len(transactions), 25):
        chunk = transactions[i:i+25]

        table_data = [table_header]
        for tx in chunk:
            row = [
                str(row_number),
                getattr(tx, "transaction_id", "-"),
                getattr(tx, "timestamp", "").strftime("%Y-%m-%d %H:%M:%S") if getattr(tx, "timestamp", None) else "-",
                tx.transaction_type.upper(),
                f"${tx.amount:,.2f}"
            ]
            table_data.append(row)
            row_number += 1

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
        ]))

        elements.append(table)

        if i + 25 < len(transactions):
            elements.append(PageBreak())

    doc.build(elements, canvasmaker=NumberedCanvas)
    return filepath