#!/bin/bash

# Script to create a password-protected PDF from the_history_of_u.md 
# and zip all 7 levels plus the PDF into a who_r_u package

set -e  # Exit on any error

echo "=== Who R U Package Creator ==="
echo

# Check if required files exist
echo "Checking for required files..."
if [ ! -f "the_history_of_u.md" ]; then
    echo "Error: the_history_of_u.md not found!"
    exit 1
fi

# Check for all 7 level files
level_files=("01_ready_to_return.dat" "02_extended_exploration.dat" "03_cramped_canal.dat" 
             "04_energy_ethnography.dat" "05_lava_labyrinth.dat" "06_dimensional_drift.dat" 
             "07_monster_mansion.dat")

for file in "${level_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Error: Level file $file not found!"
        exit 1
    fi
done

echo "All required files found ✓"
echo

# Set hardcoded password
pdf_password="DIMARYP"
echo "Using hardcoded password for PDF protection ✓"
echo

# Store current working directory
original_dir=$(pwd)

# Create temporary directory for staging
temp_dir=$(mktemp -d)
staging_dir="$temp_dir/who_r_u"
mkdir -p "$staging_dir"

echo "Created staging directory: $staging_dir"
echo

# Step 1: Convert markdown to PDF using pandoc
echo "Converting markdown to PDF..."
pandoc "the_history_of_u.md" -o "$temp_dir/the_history_of_u_temp.pdf" \
    --pdf-engine=pdflatex \
    --variable geometry:margin=1in \
    --variable fontsize=11pt \
    --variable documentclass=article \
    --toc \
    --toc-depth=2

if [ $? -eq 0 ]; then
    echo "PDF conversion successful ✓"
else
    echo "Error: PDF conversion failed!"
    rm -rf "$temp_dir"
    exit 1
fi

# Step 2: Add password protection using qpdf
echo "Adding password protection to PDF..."
qpdf --encrypt "$pdf_password" "$pdf_password" 256 -- \
    "$temp_dir/the_history_of_u_temp.pdf" \
    "$staging_dir/the_history_of_u.pdf"

if [ $? -eq 0 ]; then
    echo "Password protection added ✓"
    rm "$temp_dir/the_history_of_u_temp.pdf"  # Remove unprotected version
else
    echo "Error: Failed to add password protection!"
    rm -rf "$temp_dir"
    exit 1
fi

# Step 3: Copy all level files to staging directory
echo "Copying level files..."
for file in "${level_files[@]}"; do
    cp "$file" "$staging_dir/"
    echo "  Copied $file ✓"
done

# Step 4: Create the zip file
echo
echo "Creating zip archive..."
output_file="who_r_u_package.zip"

# Remove existing zip if it exists
if [ -f "$output_file" ]; then
    rm "$output_file"
    echo "Removed existing $output_file"
fi

# Create zip from the staging directory
cd "$temp_dir"
zip -r "$original_dir/$output_file" "who_r_u/"
cd "$original_dir"

if [ $? -eq 0 ]; then
    echo "Zip archive created successfully ✓"
else
    echo "Error: Failed to create zip archive!"
    rm -rf "$temp_dir"
    exit 1
fi

# Clean up temporary directory
rm -rf "$temp_dir"

# Final verification
if [ -f "$output_file" ]; then
    file_size=$(du -h "$output_file" | cut -f1)
    echo
    echo "=== Package Creation Complete ==="
    echo "Output file: $output_file"
    echo "File size: $file_size"
    echo
    echo "Contents when extracted:"
    echo "  who_r_u/"
    echo "    ├── the_history_of_u.pdf (password protected)"
    for file in "${level_files[@]}"; do
        echo "    ├── $file"
    done
    echo
    echo "The PDF is password protected. You will need the password to open it."
    echo "Archive will extract to a 'who_r_u' folder containing all files."
else
    echo "Error: Package creation failed!"
    exit 1
fi
