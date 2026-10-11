import streamlit as st

from text_processor import process_text
from storage import save_crm_record

from extractor import (
    extract_key_points,
    create_key_point_labels,
    extract_action_items,
    generate_summary,
    identify_next_action,
    create_crm_record
)


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
        crm_record = create_crm_record(
            customer_name,
            summary,
            key_point_labels,
            action_items,
            next_action
        )

        save_crm_record(crm_record)


        # -------------------------------------------------
        # Output Section
        # -------------------------------------------------

        st.divider()

        st.header("Call Analysis")


        # Summary
        st.subheader("Summary")

        st.info(summary)


        # Key Discussion Points
        st.subheader("Key Discussion Points")

        for point in key_point_labels:
            st.write(f"• {point}")


        # Action Items
        st.subheader("Action Items")

        for action in action_items:
            st.write(f"• {action}")


        # Next Action
        st.subheader("Next Action")

        st.success(next_action)


        # CRM Status
        st.subheader("CRM Status")

        st.write(crm_record["CRM Status"])