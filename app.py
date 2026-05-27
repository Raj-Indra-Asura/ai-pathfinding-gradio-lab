"""
AI Pathfinding Laboratory - Main Application Entry Point

This is an educational repository for learning pathfinding algorithms,
heuristic search, visualization, and benchmarking with a Gradio interface.

Run this file to launch the interactive web application:
    python app.py
"""

from src.pathfinding_lab.ui.gradio_app import create_gradio_interface


def main():
    """Launch the Gradio application."""
    demo = create_gradio_interface()

    # Launch the interface
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )


if __name__ == "__main__":
    main()
