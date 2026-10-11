def extract_key_points(sentences):
    """
    Identify important discussion points from sales-call sentences.
    """

    key_points = []

    keywords = [
        "interested",
        "requirement",
        "pricing",
        "price",
        "demo",
        "product",
        "feature",
        "requested",
    ]

    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence:
                key_points.append(sentence)
                break

    return key_points

def create_key_point_labels(key_points):
    """
    Convert extracted sentences into concise and unique key-point labels.
    """

    labels = []

    for point in key_points:

        if "pricing" in point or "price" in point:
            labels.append("Pricing discussion")

        if "demo" in point:
            labels.append("Product demo")

        if "reporting" in point:
            labels.append("Reporting requirement")

        if "feature" in point:
            labels.append("Product feature discussion")

        if "interested" in point:
            labels.append("Customer interest")

        if not any(
            keyword in point
            for keyword in [
                "pricing",
                "price",
                "demo",
                "reporting",
                "feature",
                "interested",
            ]
        ):
            labels.append("General discussion")

    # Remove duplicate labels while preserving their order
    unique_labels = list(dict.fromkeys(labels))

    return unique_labels


def extract_action_items(sentences):
    """
    Identify and create concise action items
    from sales-call sentences.
    """

    action_items = []

    for sentence in sentences:

        # Detect pricing-related actions
        if any(word in sentence for word in [
            "pricing", "price", "cost"
        ]) and any(word in sentence for word in [
            "send", "share", "provide"
        ]):
            action_items.append(
                "Send pricing information"
            )

        # Detect product demo actions
        if "demo" in sentence and any(
            word in sentence
            for word in ["requested", "schedule", "arrange"]
        ):
            action_items.append(
                "Schedule product demo"
            )

        # Detect follow-up actions
        if "follow up" in sentence or "follow-up" in sentence:
            action_items.append(
                "Follow up with customer"
            )

        # Detect information-sharing actions
        if "share" in sentence and not any(
            word in sentence
            for word in ["pricing", "price", "cost"]
        ):
            action_items.append(
                "Share requested information"
            )

        # Detect confirmation actions
        if "confirm" in sentence:
            action_items.append(
                "Confirm details"
            )

    # Remove duplicate actions while preserving order
    action_items = list(dict.fromkeys(action_items))

    return action_items


def generate_summary(sentences):
    """
    Generate a concise summary from important sales-call sentences.
    """

    summary_sentences = []

    for sentence in sentences:

        if "interested" in sentence:
            summary_sentences.append(
                "Customer is interested in the discussed product or feature."
            )

        if "pricing" in sentence or "price" in sentence:
            summary_sentences.append(
                "Pricing was discussed with the customer."
            )

        if "demo" in sentence:
            summary_sentences.append(
                "A product demo was requested."
            )

        if "send" in sentence:
            summary_sentences.append(
                "Pricing or requested information needs to be sent to the customer."
            )

    # Remove duplicate sentences
    summary_sentences = list(dict.fromkeys(summary_sentences))

    return " ".join(summary_sentences)


def create_crm_record(
    customer_name,
    summary,
    key_points,
    action_items,
    next_action
):
    """
    Create a structured CRM record from processed sales-call information.
    """

    crm_record = {
        "Customer Name": customer_name,
        "Summary": summary,
        "Key Points": key_points,
        "Action Items": action_items,
        "Next Action": next_action,
        "CRM Status": "Follow-up Required"
    }

    return crm_record

def identify_next_action(action_items):
    """
    Identify the most appropriate next action
    from the extracted action items.
    """

    if not action_items:
        return "No follow-up action identified"

    if "Schedule product demo" in action_items:
        return "Confirm demo date"

    if "Send pricing information" in action_items:
        return "Follow up with customer"

    if "Follow up with customer" in action_items:
        return "Follow up with customer"

    return action_items[0]

test_sentences = [
    "customer is interested in the reporting feature.",
    "they asked about pricing and requested a product demo.",
    "sales representative will send pricing information.",
]

key_points = extract_key_points(test_sentences)

key_point_labels = create_key_point_labels(key_points)

action_items = extract_action_items(test_sentences)

next_action = identify_next_action(action_items)

summary = generate_summary(test_sentences)

crm_record = create_crm_record(
    "John Smith",
    summary,
    key_point_labels,
    action_items,
    next_action
)

print("\nCRM Record:")

for field, value in crm_record.items():
    print(f"{field}: {value}")


print("Key Points:")

for point in key_point_labels:
    print("-", point)


print("\nAction Items:")

for action in action_items:
    print("-", action)


print("\nNext Action:")
print(next_action)


print("\nSummary:")
print(summary)