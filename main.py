import gradio as gr
from utils import preprocess_input, make_prediction

def predict_price(Brand, Type, Condition, Size=None, Title=None):
    input_dict = preprocess_input(Brand, Type, Condition, Size, Title)

    price_prediction = make_prediction(input_dict)

    return f"Predicted Price: ${price_prediction:.2f}"

# Create a Gradio interface
iface = gr.Interface(
    fn=predict_price,
    inputs=["text", "text", "text", "text", "text"],  # Adjust input types accordingly
    outputs="text",
    title="Price Prediction Interface",
    description="Predict price based on Vendor, Type, Condition, Size, and Title."
)

# Launch the interface
iface.launch(share=True)
