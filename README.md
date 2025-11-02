# huffmanTree-Ui
A simple yet powerful Python-based application to demonstrate the Huffman Coding Algorithm — implemented with Gradio for an interactive web UI and Graphviz for visualizing the Huffman Tree.
Overview
---
This project showcases how Huffman Coding, a popular greedy algorithm used in data compression, works in practice.
It takes an input string, calculates character frequencies, generates Huffman codes, computes compression efficiency, and visualizes the tree structure.

The application provides:

* A Graphical User Interface (GUI) built using Gradio.

* Interactive visualization of the Huffman Tree using Graphviz.

* Real-time calculation of compression statistics (original vs. compressed size).

Features
---
✅ Text Input Interface – Enter any string and get Huffman encoding results instantly.<br>
✅ Automatic Huffman Tree Visualization – Generates and displays a tree image dynamically using Graphviz.<br>
✅ Compression Summary – Displays original bit size, compressed bit size, and space savings.<br>
✅ Character-Level Details – Shows each character’s frequency and corresponding Huffman code.<br>
✅ Preloaded Examples – Try sample strings like "hello world" or "this is a test...".<br>
✅ Fully Interactive UI – Powered by Gradio with a clean and responsive layout.<br>

# How to Run Locally
---
1. Clone into Repo
   ```
   git clone https://github.com/chsagar141/huffmanTree-Ui.git
   cd huffmanTree-Ui
   ```
2. Install Dependencies
   Make Sure You have these Requirements Satisfied
   * Graphviz  Installed - If not Use this Link to install and Add to path [Graphviz](https://graphviz.org/download/)
   * Python 3.10 + - if not use this to download [Python](https://www.python.org/downloads/)
   Now Run this Commands:
   ```
   pip install gradio graphviz
   ```
3. Run - And Open your Localhost Link
