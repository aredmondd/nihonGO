# Navigate to the theme/static_src directory
cd theme/static_src

# Run npm and Django server concurrently
npm run dev & 
cd ../..      
python3 manage.py runserver