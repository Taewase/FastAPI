:: Create a dummy file
echo This is a test file > dummy.txt

:: Add the dummy file to git
git add dummy.txt

:: Commit the dummy file
git commit -m "Add dummy test file"

:: Push to GitHub
git push origin main