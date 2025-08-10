
def process_data(data):
    df = pd.DataFrame(data)

    df['Total'] = (
        df['Program Correctness'] + 
        df.get('Code Readability', 0) + 
        df.get('Code Efficiency', 0) + 
        df.get('Documentation', 0) + 
        df.get('Assignment Specifications', 0)
    )

    cols = [
        'Team members', 
        'Program Correctness', 
        'Code Readability', 
        'Code Efficiency', 
        'Documentation', 
        'Assignment Specifications', 
        'Total', 
        'Feedback'
    ]

    existing_cols = [col for col in cols if col in df.columns]
    return df[existing_cols] 


    # Merge dictionaries with fallbacks
    try:
        # Extract feedback from both dictionaries (default to empty string if missing)
        code_feedback = code_dict.get("Feedback", "")
        output_feedback = output_dict.get("Feedback", "")

        # Concatenate feedbacks, separating with a newline if both exist
        combined_feedback = "\n".join(filter(None, [code_feedback, output_feedback]))

        # Merge the dictionaries
        merged_data = {**code_dict, **output_dict}

        # Override the Feedback field with the combined one
        merged_data["Feedback"] = combined_feedback

        # Ensure required keys are present with default 0 values
        required_final_keys = [
            "Team members",
            "Program Correctness",
            "Code Readability",
            "Code Efficiency",
            "Documentation",
            "Assignment Specifications",
            "Consolidated Feedback",
        ]

        for key in required_final_keys:
            if key not in merged_data:
                merged_data[key] = 0  # Default fallback

        # Compute derived score
        merged_data["Program Correctness"] = (
            merged_data.get("Output for FantaxySky Drone Air Show Summary", 0) +
            merged_data.get("Output for Top 5 of 10 programs", 0)
        )

        data.append(merged_data)



    except Exception as e:
        st.error(f"Error merging evaluations: {e}")   
                    
   # Merge dictionaries with fallbacks
    try:
        # Extract feedback from both dictionaries (default to empty string if missing)
        code_feedback = code_dict.get("Feedback", "")
        output_feedback = output_dict.get("Feedback", "")

        # Concatenate feedbacks, separating with a newline if both exist
        combined_feedback = "\n".join(filter(None, [code_feedback, output_feedback]))

        # Merge the dictionaries
        merged_data = {**code_dict, **output_dict}

        # Override the Feedback field with the combined one
        merged_data["Feedback"] = combined_feedback

        # Ensure required keys are present with default 0 values
        required_final_keys = [
            "Team members",
            "Program Correctness",
            "Code Readability",
            "Code Efficiency",
            "Documentation",
            "Assignment Specifications",
            "Consolidated Feedback",
        ]

        for key in required_final_keys:
            if key not in merged_data:
                merged_data[key] = 0  # Default fallback

        data.append(merged_data)

    except Exception as e:
        st.error(f"Error merging evaluations: {e}")   
                    
# Final DataFrame processing
if data:
    # write to dataframe
    df = process_data(data)
    st.write(df)
