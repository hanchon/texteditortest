cd frontend
gnome-terminal -- npm run serve
cd ../backend 
source .venv/bin/activate
uvicorn main:app --reload

