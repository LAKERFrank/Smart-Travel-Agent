import tqdm
import gradio as gr
from huggingface_hub import InferenceClient

from gemini_api import get_travel_info, get_travel_recommendations
from pdf_convert import markdown_to_pdf_weasyprint

def generate_response(input_text):
    user_query = input_text.strip()
    if not user_query:
        print("Please enter a valid travel query!")
        return

    travel_info = get_travel_info(user_query)

    if travel_info and travel_info.get("to") and travel_info.get("from"):
        travel_recommendations = get_travel_recommendations(
            travel_info.get("intent"),
            travel_info.get("from"),
            travel_info.get("to"),
            travel_info.get("departure_date"),
            travel_info.get("duration"),
            travel_info.get("budget"),
            travel_info.get("num_people"),
        )
        pdf = markdown_to_pdf_weasyprint(travel_recommendations)
    else:
        print("Could not extract travel information. Please refine your query.")

    return pdf

with gr.Blocks() as demo:
    gr.Markdown("## PDF Processing with Gemini API")
    message = "I want to plan a trip from Taiwan to Tokyo for 5 days with a budget of $10000 for 2 people, leaving on March 1st."
    input_text = gr.Textbox(label="User Request", value=message, placeholder="Enter your travel detail here")
    submit = gr.Button("Generate")
    output_pdf = gr.File(label="Download Output PDF")

    submit.click(fn=generate_response, inputs=input_text, outputs=output_pdf)


if __name__ == "__main__":
    demo.launch(ssr_mode=False)
