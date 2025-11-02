import heapq
from collections import Counter
import gradio as gr
import graphviz
import os

# --- (Optional) Set up Graphviz environment variable ---
# If you installed Graphviz to a custom location, you might need to
# add its 'bin' directory to the system's PATH.
# Example: os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'


# --- 1. BACKEND: Huffman Algorithm Logic ---

class Node:
    """A node for the Huffman Tree."""

    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        """Compares nodes based on frequency (for the priority queue)."""
        return self.freq < other.freq


def build_huffman_tree(text):
    """
    Builds the Huffman tree from a text string.
    Returns the root node and a dictionary of character frequencies.
    """

    if not text:
        return None, {}

    frequencies = Counter(text)

    priority_queue = []
    for char, freq in frequencies.items():
        node = Node(char, freq)
        heapq.heappush(priority_queue, node)

    if len(priority_queue) == 1:
        node = heapq.heappop(priority_queue)
        parent_node = Node(None, node.freq, node, None)
        heapq.heappush(priority_queue, parent_node)

    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)

        merged_freq = left_child.freq + right_child.freq
        parent_node = Node(None, merged_freq, left_child, right_child)

        heapq.heappush(priority_queue, parent_node)

    root_node = heapq.heappop(priority_queue)

    return root_node, frequencies


def generate_huffman_codes(text):
    """
    Main function to build the tree and generate the codes.
    Returns the codes dictionary, the frequencies dictionary, and the tree's root_node.
    """

    root_node, frequencies = build_huffman_tree(text)

    if root_node is None:
        return {}, {}, None

    codes = {}

    def _get_codes_recursive(node, current_code=""):
        """Recursive helper function to traverse the tree and build codes."""
        if node is None:
            return

        if node.char is not None:
            if not current_code:
                codes[node.char] = "0"
            else:
                codes[node.char] = current_code
            return

        _get_codes_recursive(node.left, current_code + "0")
        _get_codes_recursive(node.right, current_code + "1")

    _get_codes_recursive(root_node)

    return codes, frequencies, root_node

# --- 2. BACKEND: Visualization Logic ---


def visualize_tree(root_node):
    """
    Creates a Graphviz Digraph object and renders it to a PNG file.
    Returns the file path.
    """
    if root_node is None:
        return None

    try:
        dot = graphviz.Digraph(comment='Huffman Tree')
        dot.attr('node', shape='record', style='rounded')

        internal_node_counter = 0

        def add_nodes_edges(node, node_id):
            nonlocal internal_node_counter

            if node.char is not None:
                char_display = repr(node.char).strip("'")
                label = f"{{ {char_display} | Freq: {node.freq} }}"
                dot.node(node_id, label=label, shape='record')
            else:
                label = f"{{ <f0> | Freq: {node.freq} | <f1> }}"
                dot.node(node_id, label=label, shape='Mrecord')

            if node.left:
                if node.left.char is None:
                    internal_node_counter += 1
                    left_id = f"internal_{internal_node_counter}"
                else:
                    left_id = repr(node.left.char)

                add_nodes_edges(node.left, left_id)

                if node.char is not None:
                    dot.edge(node_id, left_id, label='0')
                else:
                    dot.edge(f"{node_id}:f0", left_id, label='0')

            if node.right:
                if node.right.char is None:
                    internal_node_counter += 1
                    right_id = f"internal_{internal_node_counter}"
                else:
                    right_id = repr(node.right.char)

                add_nodes_edges(node.right, right_id)

                if node.char is not None:
                    dot.edge(node_id, right_id, label='1')
                else:
                    dot.edge(f"{node_id}:f1", right_id, label='1')

        add_nodes_edges(root_node, "root")

        # Render the graph to a temporary PNG file and return the path
        temp_file_path = dot.render(
            filename='huffman_tree', format='png', cleanup=True)
        return temp_file_path

    except Exception as e:
        print(f"Error during graphviz visualization: {e}")
        print("Please ensure Graphviz is installed and in your system's PATH.")
        return None


# --- 3. FRONTEND: Gradio Interface Logic ---

def huffman_utility(input_text):
    """
    The main function called by the Gradio interface.
    Takes user input, runs the Huffman logic, and formats the outputs.
    """

    if not input_text:
        # Return empty/default values for all 4 outputs
        return None, "N/A", "N/A", None

    # --- Run the backend logic ---
    codes, frequencies, root_node = generate_huffman_codes(input_text)

    # --- 1. Prepare DataFrame Output ---
    dataframe_data = []
    sorted_freqs = sorted(frequencies.items(),
                          key=lambda item: item[1], reverse=True)

    for char, freq in sorted_freqs:
        char_display = repr(char).strip("'")  # Use repr for special chars
        row = [char_display, freq, codes.get(char, "N/A")]
        dataframe_data.append(row)

    # --- 2. Calculate Size Comparison ---
    # Assuming 8 bits per char (ASCII)
    original_size_bits = len(input_text) * 8

    compressed_size_bits = 0
    for char, freq in frequencies.items():
        compressed_size_bits += len(codes.get(char, "")) * freq

    original_size_str = f"{original_size_bits} bits ({len(input_text)} chars * 8 bits/char)"

    savings = original_size_bits - compressed_size_bits
    savings_percent = (savings / original_size_bits *
                       100) if original_size_bits > 0 else 0

    compressed_size_str = f"{compressed_size_bits} bits (Savings: {savings} bits | {savings_percent:.2f}%)"

    # --- 3. Generate Tree Visualization ---
    tree_image_path = visualize_tree(root_node)

    # Return the four outputs in the correct order
    return dataframe_data, original_size_str, compressed_size_str, tree_image_path


# --- 4. Launch the Application (Using gr.Blocks) ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📊 Huffman Coding Utility")
    gr.Markdown("Enter a string to see its Huffman codes and compression results. This demonstrates the greedy algorithm from your syllabus (Module IV).")

    # Define the input component
    text_input = gr.Textbox(
        label="Enter your text here",
        placeholder="Type something to compress...",
        lines=3
    )

    # Define the Submit button
    submit_btn = gr.Button("Generate")

    # Define the output components
    dataframe_output = gr.Dataframe(
        label="📊 Huffman Codes",
        headers=["Character", "Frequency", "Huffman Code"],
        datatype=["str", "number", "str"]
    )

    # Use gr.Row for the side-by-side layout
    with gr.Row():
        original_size_output = gr.Textbox(label="📦 Original Size (ASCII)")
        compressed_size_output = gr.Textbox(label="📬 Compressed Size")

    tree_output = gr.Image(
        label="🌲 Huffman Tree Visualization", type="filepath")

    # Add examples
    gr.Examples(
        examples=[["hello world"], [
            "this is a test of the huffman coding algorithm"], ["AAAAABBBCC"]],
        inputs=text_input,
        outputs=[dataframe_output, original_size_output,
                 compressed_size_output, tree_output],
        fn=huffman_utility,
        cache_examples=False  # Disable caching for file-based outputs
    )

    # Connect the button click to the function
    submit_btn.click(
        fn=huffman_utility,
        inputs=text_input,
        outputs=[dataframe_output, original_size_output,
                 compressed_size_output, tree_output]
    )

# Run the app
if __name__ == "__main__":
    print("Launching Gradio UI... (Access it at the URL below)")
    demo.launch()
