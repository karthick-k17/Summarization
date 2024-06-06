def calculate_keyword_percentage(summary, key_terms):
    words = summary.lower().split()
    key_term_count = sum(1 for word in words if word in key_terms)
    percentage = (key_term_count / len(words)) * 100
    return percentage

def validate(summary1, summary2, keywords):
    percentage1 = calculate_keyword_percentage(summary1, keywords)
    percentage2 = calculate_keyword_percentage(summary2, keywords)
    
    print(f"Summary 1 Key Term Percentage: {percentage1:.2f}%")
    print(f"Summary 2 Key Term Percentage: {percentage2:.2f}%")
    
    if percentage1 > percentage2:
        print("Summary 1 is more relevant based on key terms.")
    else:
        print("Summary 2 is more relevant based on key terms.")
