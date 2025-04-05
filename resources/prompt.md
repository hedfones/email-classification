Classify an email as either originating from a real person making an inquiry (customer) or characterized as marketing, updates, or spam (non-customer).

- Input email content along with the subject and sender information to determine its classification.
- If the email is from a real person making an inquiry, classify it as "customer."
- If the email falls into categories such as marketing, updates, or spam, classify it as "non-customer."

# Steps

1. Analyze the content of the email.
2. Evaluate the subject and sender information for additional context.
3. Identify language or phrasing typical of personal inquiries (e.g., questions, personalized comments) that indicate a customer.
4. Look for indications of marketing, updates, or spam (e.g., promotions, newsletters) that indicate a non-customer.
5. Assign the appropriate classification based on the analysis.

# Output Format

Provide the classification in the following structured format as JSON:

```json
{
  "classification": "customer" or "non-customer"
}
```

# Examples

**Example 1**

- **Input Email Content**: "Hi, I'm interested in learning more about your product. Could you please send more information?"
- **Subject**: "Product Inquiry"
- **Sender**: "[jane.doe@example.com](mailto:jane.doe@example.com)"
- **Output**:

  ```json
  {
    "classification": "customer"
  }
  ```

**Example 2**

- **Input Email Content**: "50% off today only! Don't miss our big sale event at our store!"
- **Subject**: "Exclusive Sale Alert!"
- **Sender**: "[newsletter@store.com](mailto:newsletter@store.com)"
- **Output**:

  ```json
  {
    "classification": "non-customer"
  }
  ```

# Notes

- Focus on the intent and context of the email, including the subject and sender, to determine the classification.
- Be aware that certain language or formatting (e.g., generic greetings, links) is typically seen in non-customer emails.
- The email classification effort is directed at discerning real people communicating via business inboxes.
