import streamlit as st

from text_processor import process_text
from storage import save_crm_record

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from xml.sax.saxutils import escape

from extractor import (
    extract_key_points,
    create_key_point_labels,
    extract_action_items,
    generate_summary,
    identify_next_action,
    create_crm_record
)

def generate_pdf_report(
    customer_name,
    call_notes,
    cleaned_text,
    summary,
    key_points,
    action_items,
    next_action,
    crm_status
):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch
    )

    styles = getSampleStyleSheet()
    story = []

    # Report title
    story.append(
        Paragraph(
            "Sales Call Analysis Report",
            styles["Title"]
        )
    )
    story.append(Spacer(1, 12))

    def add_section(title, content):
        story.append(
            Paragraph(title, styles["Heading2"])
        )
        story.append(Spacer(1, 5))

        # Escape special HTML characters and preserve line breaks
        safe_content = escape(str(content or "Not available"))
        safe_content = safe_content.replace("\n", "<br/>")

        story.append(
            Paragraph(safe_content, styles["BodyText"])
        )
        story.append(Spacer(1, 12))

    add_section("Customer / Prospect", customer_name)
    add_section("Original Call Notes", call_notes)
    add_section("Cleaned Notes", cleaned_text)
    add_section("Conversation Summary", summary)

    add_section(
        "Key Discussion Points",
        "\n".join(f"- {point}" for point in key_points)
        if key_points else "No key points identified."
    )

    add_section(
        "Action Items",
        "\n".join(f"- {item}" for item in action_items)
        if action_items else "No action items identified."
    )

    add_section("Next Recommended Action", next_action)
    add_section("CRM Record Status", crm_status)

    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            f"Generated on: {datetime.now().astimezone().strftime('%d %b %Y, %I:%M %p %Z')}",
            styles["Italic"]
        )
    )

    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Sales Call Notes Summarizer",
    page_icon="📞",
    layout="wide"
)


# -------------------------------------------------
# Application Title
# -------------------------------------------------

st.title("📞 Sales Call Notes Summarizer")

st.write(
    "Convert sales-call notes into concise summaries, "
    "key discussion points, action items, and next actions."
)


st.divider()


# -------------------------------------------------
# Input Section
# -------------------------------------------------

st.subheader("Call Information")

customer_name = st.text_input(
    "Customer / Prospect Name",
    placeholder="Enter customer name"
)

call_notes = st.text_area(
    "Sales Call Notes",
    placeholder="Enter the sales-call notes here...",
    height=200
)


process_button = st.button(
    "Process Call",
    type="primary"
)


# -------------------------------------------------
# Processing
# -------------------------------------------------

if process_button:
    
    if not customer_name.strip():
        st.warning("Please enter the Customer / Prospect Name.")

    elif not call_notes.strip():
        st.warning("Please enter the Sales Call Notes.")

    else:

        # Step 1: Process text
        cleaned_text, sentences, words = process_text(call_notes)

        # Step 2: Extract key points
        key_points = extract_key_points(sentences)

        # Step 3: Create key-point labels
        key_point_labels = create_key_point_labels(key_points)

        # Step 4: Extract action items
        action_items = extract_action_items(sentences)

        # Step 5: Identify next action
        next_action = identify_next_action(action_items)

        # Step 6: Generate summary
        summary = generate_summary(sentences)

        # Step 7: Create CRM record
        # crm_record = create_crm_record(
        #     customer_name,
        #     summary,
        #     key_point_labels,
        #     action_items,
        #     next_action
        # )

        # save_crm_record(crm_record)
        
        crm_record = create_crm_record(
            customer_name,
            summary,
            key_point_labels,
            action_items,
            next_action
        )

        # Add the original and cleaned notes
        crm_record["Original Call Notes"] = call_notes
        crm_record["Cleaned Notes"] = cleaned_text
        
        # Save the complete record
        save_crm_record(crm_record)
        
        st.success("All call information saved successfully!")


        # -------------------------------------------------
        # Output Section
        # -------------------------------------------------

        st.divider()

        st.header("Call Analysis")


        # # Summary
        # st.subheader("Summary")

        # st.info(summary)


        # # Key Discussion Points
        # st.subheader("Key Discussion Points")

        # for point in key_point_labels:
        #     st.write(f"• {point}")


        # # Action Items
        # st.subheader("Action Items")

        # for action in action_items:
        #     st.write(f"• {action}")


        # # Next Action
        # st.subheader("Next Action")

        # st.success(next_action)


        # # CRM Status
        # st.subheader("CRM Status")

        # st.write(crm_record["CRM Status"])

        
    # -------------------------------------------------
    # Professional Call Analysis Dashboard
    # -------------------------------------------------
    
    # Generate downloadable PDF
    pdf_report = generate_pdf_report(
        customer_name=customer_name.strip(),
        call_notes=call_notes,
        cleaned_text=cleaned_text,
        summary=summary,
        key_points=key_point_labels,
        action_items=action_items,
        next_action=next_action,
        crm_status=crm_record["CRM Status"]
    )
    st.download_button(
        label="📥 Download Report as PDF",
        data=pdf_report,
        file_name=(
            f"Sales_Call_Report_"
            f"{customer_name.strip().replace(' ', '_')}.pdf"
        ),
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )

    st.divider()
    
    st.markdown(
        """
        <div style="
            padding: 24px;
            border-radius: 16px;
            background: linear-gradient(120deg, #172554, #1d4ed8);
            color: white;
            margin-bottom: 22px;
        ">
            <div style="font-size: 13px; opacity: 0.85;">
                SALES INTELLIGENCE DASHBOARD
            </div>
            <h1 style="margin: 8px 0 4px 0; color: white;">
                Call Analysis
            </h1>
            <p style="margin: 0; color: #e0e7ff;">
                A clear view of the conversation, priorities and next steps.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Customer information
    st.markdown(f"### 👤 {customer_name.strip()}")
    
    st.caption("Customer / Prospect")
    
    
    # Summary card
    st.markdown("#### 📝 Conversation Summary")
    
    st.markdown(
        f"""
        <div style="
            background: #eff6ff;
            border-left: 5px solid #2563eb;
            border-radius: 10px;
            padding: 18px;
            color: #1e293b;
            line-height: 1.7;
        ">
            {summary if summary else "No summary could be generated from these notes."}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("")
    
    # Two-column results layout
    left_col, right_col = st.columns(2, gap="large")
    
    with left_col:
    
        st.markdown("#### 🎯 Key Discussion Points")
    
        if key_point_labels:
            for point in key_point_labels:
                st.markdown(
                    f"""
                    <div style="
                        background: #f0fdf4;
                        border: 1px solid #bbf7d0;
                        border-radius: 9px;
                        padding: 11px 14px;
                        margin-bottom: 9px;
                        color: #166534;
                    ">
                        ✓ &nbsp; {point}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No key discussion points identified.")
    
    with right_col:
    
        st.markdown("#### ✅ Action Items")
    
        if action_items:
            for index, action in enumerate(action_items, start=1):
                st.markdown(
                    f"""
                    <div style="
                        background: #fff7ed;
                        border: 1px solid #fed7aa;
                        border-radius: 9px;
                        padding: 11px 14px;
                        margin-bottom: 9px;
                        color: #9a3412;
                    ">
                        <b>{index}.</b> &nbsp; {action}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No action items identified from these notes.")
    
    st.write("")
    
    # Next action and CRM status
    next_col, status_col = st.columns(2, gap="large")
    
    with next_col:
        st.markdown(
            """
            <div style="
                background: #f5f3ff;
                border: 1px solid #ddd6fe;
                border-radius: 12px;
                padding: 18px;
                min-height: 125px;
            ">
                <div style="font-size: 13px; color: #6d28d9;">
                    NEXT STEP
                </div>
                <div style="
                    font-size: 19px;
                    font-weight: 600;
                    color: #4c1d95;
                    margin-top: 12px;
                ">
                    Follow-up recommendation
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.info(next_action)
    
    with status_col:
        st.markdown(
            """
            <div style="
                background: #fefce8;
                border: 1px solid #fde68a;
                border-radius: 12px;
                padding: 18px;
                min-height: 125px;
            ">
                <div style="font-size: 13px; color: #854d0e;">
                    CRM RECORD STATUS
                </div>
                <div style="
                    font-size: 19px;
                    font-weight: 600;
                    color: #713f12;
                    margin-top: 12px;
                ">
                    Follow-up tracking
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.warning(crm_record["CRM Status"])
    
    # Saved record confirmation
    st.success(
        "Call analysis completed and CRM information saved to CSV."
    )
    