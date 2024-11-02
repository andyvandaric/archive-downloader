# Archive Downloader

**Python Archive Downloader** is a specially designed tool for efficiently performing bulk downloads from [Archive.org](https://archive.org/). 

Utilizing an Archive.org Downloader script, this tool leverages the capabilities of a *multi-threaded downloader in Python* to significantly enhance download speeds. With the help of **aria2c**, which acts as an **aria2c downloader Python script**, you can enjoy a fast and reliable downloading experience. Additionally, the project includes a *BeautifulSoup download script* to facilitate easy data extraction from web pages.

As a **command-line download tool**, users can effortlessly access various advanced features, including **rich CLI logging in Python** to provide informative and easy-to-read logs during the download process. 

This tool also offers Archive.org multi-file download capabilities, allowing you to download multiple files simultaneously without hassle. With the integration of a **download JSON indexing script**, you can easily manage and organize the data being downloaded. 

All these features make this **Python high-speed downloader** an excellent choice for anyone looking to become an **Archive.org batch downloader** in a straightforward and enjoyable manner.

---

## Features

Archive Downloader comes packed with powerful features that make it stand out:

1. **Object-Oriented Structure**: This tool is organized with modular, object-oriented design using Python classes, making the codebase easy to understand, debug, and extend for additional functionalities.

2. **Customizable Base URL and Download Directory**: Users can specify the `base_url` and `project_dir` for each download, allowing for flexibility and systematic file organization.

3. **Efficient Logging Management**: Configures both console and file-based logging with `RichHandler`, providing rich, color-coded logs in the terminal and detailed logs saved to a file, making debugging and tracking simple.

4. **Automatic Directory Creation**: Automatically creates required directories based on the `base_url`, organizing downloaded files into a clear folder structure.

5. **Robust Error Handling**: Handles errors gracefully with clear error logs, ensuring smooth script execution even when encountering network or file-related issues.

6. **Parallel Download Support**: Uses `concurrent.futures` for multi-threading, enabling faster downloads when multiple files are present. The `get_optimal_threads` method dynamically adjusts thread count based on CPU load to prevent excessive system usage.

7. **High-Speed Downloads with aria2c**: Utilizes `aria2c` for fast, stable downloads. Supports multi-connection downloads that break files into smaller parts for concurrent downloading.

8. **Progress Visualization with tqdm**: Displays a real-time progress bar during downloads, helping users track progress, especially useful for large or multiple files.

9. **Keyboard Interrupt for Quick Abort**: Users can press `CTRL + X` to instantly abort the download process, providing greater control in case of accidental downloads or changes in priority.

10. **Automatic Index Creation**: Generates an `index.json` file after downloads, listing all downloaded files with metadata, making it easy to reference, document, or expand upon for future use.

11. **User-Friendly Interface with Typer**: Integrates with `Typer` for a simple and intuitive command-line interface, displaying error messages and usage prompts for enhanced user experience.

12. **Enhanced Output with Rich**: Uses `rich` for color-coded terminal outputs, making download statuses clear and readable. The statuses include "Downloaded," "Already exists," and "Error."

13. **Intelligent File Filtering**: Scrapes and filters files from the Archive.org download page using `BeautifulSoup`, ensuring only the desired files are downloaded, saving time and storage.

14. **Cross-Platform Compatibility and Scalability**: Compatible with multiple operating systems and scalable for various types of projects, making it a versatile tool for bulk downloads.

---

## Prerequisites

- **Python 3.7 or higher**
- **aria2c**: Download manager for optimized file transfers
- **BeautifulSoup**: HTML parsing library
- **Rich**: Enhanced console logging
- **Typer**: Command-line interface generation
- **TQDM**: Progress bar for terminal
- **psutil**: CPU usage tracking

---

## Installation Guide

Follow these steps to install and run **Python Archive Downloader** on all operating systems:

### 1. Clone Repository GitHub

First, you need to clone this repository to your local machine. Open your terminal (Command Prompt on Windows, Terminal on macOS or Linux) and run the following command:

```bash
git clone https://github.com/andyvandaric/archive-downloader.git 

cd archive-downloader
```

### 2. Instal Python 3.12.2

If you haven't installed Python 3.12.2 yet, you can download it from the [official Python website](https://www.python.org/downloads/). Choose the version that suits your operating system and follow the installation instructions:

- **Windows**: Download the installer and run it. Be sure to check the option "Add Python to PATH".

- ****macOS**: You can use Homebrew to install Python with the following command:
  
  ```bash
  brew install python@3.12
  ```

- **Linux**: You can use your package manager. For example, on Ubuntu, use:
  
  ```bash
  sudo apt update sudo apt install python3.12
  ```

### 3. Instal Poetry

Poetry is a dependency management and packaging tool for Python.

#### Linux & Mac OS

Install Poetry by running the following command in the terminal:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Windows Powershell

**Run PowerShell as Administrator**:

- Right-click on the PowerShell icon and select **Run as administrator**. This will provide higher access rights and can resolve permission issues.

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicP | Invoke-Expression)
```

After the installation is complete, make sure to add Poetry to your PATH by following the on-screen instructions.

### 4. Enter the Poetry Shell

Once Poetry is installed, you can enter the Poetry shell with the following command:

```bash
poetry shell
```

### 5. Install Required Libraries

Using Poetry, you can install all the necessary dependencies with the following command:

```bash
poetry install
```

Once in the Poetry shell, you can install all the packages at once with the following command:

```bash
poetry add requests beautifulsoup4 rich typer tqdm psutil keyboard
```

### 6. Pastikan `aria2c` Terinstal

Make sure you also install `aria2c` on your system. You can install it according to your operating system:

- **Linux**:
  
  ```bash
  sudo apt install aria2
  ```

- **MacOS**:
  
  ```bash
  brew install aria2`
  ```

- **Windows**: Download from [Aria2 Releases](https://github.com/aria2/aria2/releases) and follow the installation instructions.
  
  - Download `aria2c` To install `aria2c` on Windows, download the ZIP file for the 64-bit version from [Aria2 Releases](https://github.com/aria2/aria2/releases/latest/download/aria2-1.37.0-win-64bit-build1.zip).
  
  - Extract the Files
    After downloading, extract the files to the following folder: `C:\Program Files\aria2`
  
  - Add to Environment Variables
    
    - **Open System Settings**:
      
      - Right-click on **This PC** or **Computer** in File Explorer, then select **Properties**.
      
      - Click on **Advanced system settings** on the left panel.
      
      - In the **System Properties** tab, click the **Environment Variables** button.
      
      - **Edit PATH**:
        
        - Under **System variables**, find and select the variable named `Path`, then click **Edit**.
        
        - Click **New** and add the folder location of `aria2` that you extracted:
          
          `C:\Program Files\aria2`
        
        - Click **OK** to save the changes.
      
      - **Edit PATH for User** (optional, if you want access for specific users):
        
        - Under **User variables**, repeat the same steps to add the location to PATH.
  
  - Verify `aria2` Installation
    
    After setting the PATH, open a new Command Prompt and run the following command to verify that `aria2c` is installed correctly:
    
    - ```
      aria2c --version
      ```
      
      If `aria2c` is installed correctly, you should see the version displayed in the terminal.

## Usage

```bash
python archive_downloader.py <BASE_URL>
```

Replace `<BASE_URL>` with the URL from Archive.org that you want to download files from. 

For example:

```bash
python archive_downloader.py https://archive.org/details/some-content-id
```

### Script Workflow

1. **Initialization**: The script initiates with the `base_url` and a customizable `project_dir` to store downloaded files.
2. **Directory and Log Setup**: Sets up the necessary directories and logging configurations.
3. **File List Retrieval**: Uses `BeautifulSoup` to scrape file details from the Archive.org download page.
4. **Parallel Downloads**: Executes downloads in parallel using optimized threads.
5. **Real-Time Progress**: Displays download progress with `tqdm`.
6. **Index Creation**: Creates an `index.json` file listing all downloaded files with their metadata.

---

## Detailed Features and Benefits

- **Speed and Efficiency**: Archive Downloader's multi-threading and `aria2c` enable faster downloads, perfect for large collections.
- **Flexible and Scalable**: Suitable for diverse projects, adaptable to various file types, with organized output.
- **Real-Time Monitoring**: With `tqdm` progress bars and `Rich` terminal outputs, users have real-time feedback on download statuses.
- **Error Resilience**: Intelligent error handling, logging, and recovery mechanisms ensure robust, uninterrupted downloads.
- **Indexing and Documentation**: Automatically generates a JSON index of all downloaded files, facilitating organization and documentation.
- **User Control**: Abort downloads on demand with `CTRL + X`, giving full control to the user.

---

## Example Use Cases

The **Python Archive Downloader** offers a versatile solution for efficiently accessing and managing a wide array of digital content from [Archive.org](https://archive.org). Whether you're involved in academic research, creative projects, or technical development, this tool enables users to **bulk download from Archive.org** effortlessly. With features like **multi-threaded downloading** and support for various file types, it serves as an invaluable resource for anyone looking to preserve digital content or streamline their data acquisition processes. Below are some practical use cases that demonstrate the diverse applications of this powerful **Archive.org downloader script**.

### **Archiving and Digital Preservation**:

- **Archiving Large Audio/Video Collections**: Download entire collections from Archive.org efficiently, ensuring that valuable media is preserved for future generations.
- **Digital Preservation**: Collect and preserve endangered digital content, such as outdated software or obsolete web pages, for future access and research.
- **Cultural Heritage Preservation**: Gather and preserve digital artifacts, folklore, and oral histories that contribute to cultural heritage documentation and education.

### **Research and Academia**:

- **Data Analysis Projects**: Quickly download large datasets for data analysis or machine learning projects, streamlining the process of obtaining the necessary data for research.
- **Academic Research**: Gather relevant historical documents, research papers, and multimedia resources from Archive.org to support thesis and dissertation work.
- **Historical Research**: Gather primary sources, including newspapers, photographs, and documents, to support historical research projects and publications.
- **Environmental Research**: Download historical climate data or ecological studies from Archive.org to aid in research and analysis of environmental changes over time.
- **Genealogy Projects**: Collect historical records and archives that assist in genealogical research, allowing individuals to trace their ancestry and family history.

### **Creative Projects and Content Creation**:

- **Content Creation**: Source materials for video production, podcasts, or blog posts by downloading relevant media files and incorporating them into creative projects.
- **Creative Writing**: Access archived literary works and anthologies to inspire creative writing projects or to study different writing styles and genres.
- **Podcasting**: Download and curate audio recordings from historical speeches or radio shows to enrich podcast content or provide context for discussions.
- **Art and Design Projects**: Access a wide range of artistic works and historical design archives to inspire and inform contemporary art and design projects.

### **Educational Resource Collection**:

- **Educational Resource Collection**: Download educational videos, textbooks, and lecture notes from Archive.org to create comprehensive study materials for students and educators.
- **Library Resource Compilation**: Assist librarians in compiling resources for patrons by downloading specific collections or archives that align with community interests.

### **Technical and Developmental Projects**:

- **Open Source Development**: Retrieve archived software projects or documentation to support open-source contributions or revitalize abandoned projects.
- **Game Development**: Download archived games, demos, and their assets to study game design and mechanics or to use as references in new game projects.
- **Web Development**: Retrieve archived websites to analyze design trends, user experience, and content strategies over the years for inspiration in modern web development.

### **Social Research and Analysis**:

- **Social Media Content**: Collect archived social media posts and content for analysis, helping researchers study trends and public sentiment over time.
- **Event Documentation**: Download recordings and materials from conferences or webinars hosted on Archive.org to create a repository of knowledge for attendees and future learners.

### **Corporate and Market Research**:

- **Corporate Research**: Compile historical business documents, advertisements, and promotional materials to support market research and business analysis.

### **Language Learning**:

- **Language Learning**: Download audio and video resources in various languages to enhance language acquisition and cultural understanding through immersive content.

---

## Frequently Asked Questions about the Python Archive Downloader

In this section, we address some common inquiries regarding the **Python Archive Downloader** and its capabilities. Whether you're interested in using this **Archive.org downloader script** for academic research, bulk downloads, or media preservation, these FAQs provide valuable insights to help you make the most of this powerful tool.

### **1. What is the Python Archive Downloader?**

The Python Archive Downloader is a command-line tool designed to facilitate efficient downloading of files from Archive.org. It supports multi-threading for high-speed downloads and allows users to organize and manage their downloaded files effectively.

### **2. How can I bulk download files from Archive.org?**

Using the Python Archive Downloader, you can bulk download files by specifying collection URLs or search parameters. The tool utilizes `aria2c` for enhanced download speeds and can handle multiple files simultaneously.

### **3. What types of files can I download with this tool?**

The downloader supports a variety of file types, including audio, video, images, documents, and software. You can download complete collections or individual files as needed.

### **4. Is there a way to preserve metadata during downloads?**

Yes! The Python Archive Downloader is designed to automatically organize downloaded files and preserve associated metadata, making it easier to create local backups and maintain the integrity of your collections.

### **5. Can I use this tool for academic or research purposes?**

Absolutely! The downloader is particularly useful for academic research, allowing users to gather historical documents, datasets, and multimedia resources for analysis or project support.

### **6. How does the multi-threaded downloading feature work?**

The multi-threaded downloading feature enables the tool to initiate multiple download threads simultaneously, significantly increasing the speed and efficiency of the download process, especially for large collections.

### **7. Is there any support for using this tool in game development?**

Yes, the Python Archive Downloader can be utilized in game development to download archived games, demos, and their assets, allowing developers to study design mechanics or utilize resources for their projects.

### **8. Are there any language learning resources available on Archive.org?**

Yes, Archive.org hosts a variety of audio and video resources in multiple languages that can be downloaded using the Python Archive Downloader, making it a valuable tool for language learners.

### **9. How can I get started with the Python Archive Downloader?**

To get started, simply install the tool, configure your environment, and refer to the user documentation for instructions on how to use the various features effectively.

### **10. Where can I find help if I encounter issues?**

For any issues or questions, you can refer to the official documentation, check community forums, or reach out for support through the project's GitHub repository.

---

## Troubleshooting

- **Error in Download**: Ensure `aria2c` is installed and accessible in your system’s PATH.
- **Incorrect URL Format**: Make sure the `base_url` includes "details" or "download".
- **Permission Issues**: Run the script in a directory where you have write permissions.

For further assistance, please submit an issue on our [GitHub repository](https://github.com/andyvandaric/archive-downloader).

---

## License

This project is licensed under the MIT License. See the [LICENSE file](https://github.com/andyvandaric/archive-downloader/blob/main/LISENSE.md) for more details.

## Contributions

Contributions are welcome! Please fork the repository and create a pull request with detailed descriptions of changes. For major changes, please open an issue first to discuss.

---

## Author

Developed by [andyvandaric](https://github.com/andyvandaric). If you have questions or feedback, feel free to reach out!

This **README.md** includes all necessary details, user instructions, SEO-friendly keywords, and additional sections to align with industry standards for open-source projects. Let me know if you need further customization!
