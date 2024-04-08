The provided tool is a directory scanner designed to search for directories on a web server. Here's a review of the tool and instructions on how to use it:

### Tool Review:

1. **Features**:
   - Scans a target web server for directories based on a provided wordlist.
   - Allows customization of file extensions to search for within directories.
   - Supports specifying the HTTP method to use for scanning.
   - Utilizes multithreading for faster scanning.
   - Outputs discovered directories along with their status codes to a timestamped text file.

2. **Pros**:
   - Customizable: Users can specify various parameters like file extensions, HTTP method, number of threads, etc.
   - Multithreaded: Utilizes threading to improve the scanning speed.
   - Error Handling: Gracefully handles exceptions during scanning.

3. **Cons**:
   - Limited Error Reporting: The tool only prints basic error messages without providing detailed information about encountered errors.

### How to Use:

1. **Setup**:
   - Ensure Python is installed on your system.
   - Install required dependencies using `pip install requests colorama`.

2. **Usage**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script.
   - Run the script using Python: `python directory_scanner.py <target_host>`
   - Replace `<target_host>` with the URL of the target web server.
   
3. **Input Parameters**:
   - The script will prompt you to input the following parameters:
     - File extensions to search for (e.g., php, aspx, jsp).
     - Number of threads to use for scanning.
     - Path to the directory wordlist file.
     - Desired HTTP status codes (e.g., 200, 302, 404).

4. **Output**:
   - The tool will display information about the scan configuration.
   - It will then start scanning the target web server.
   - Discovered directories along with their status codes will be saved to a timestamped text file in the 'reports' directory.

5. **Review Output**:
   - After the scan completes, review the generated text file to see the discovered directories and their status codes.

6. **Further Analysis**:
   - Explore the discovered directories to identify potential security vulnerabilities or misconfigurations.
   - Investigate directories with unexpected status codes for potential issues.

7. **Additional Notes**:
   - Ensure that you have necessary permissions to perform scans on the target web server.
   - Use the tool responsibly and only on web servers you have authorization to scan.

By following these steps, you can effectively use the directory scanner tool to identify directories on a web server and analyze them for potential security risks.
