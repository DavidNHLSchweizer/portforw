start python -I ClientServer.py --p 8000 --c yellow --m "Dit is de eerste server"
start python -I ClientServer.py --p 8001 --c green --m "Dit is de tweede server"
start python -I ClientServer.py --p 8002 --c cyan --m "Dit is niet de tweede server"
start python -I ClientServer.py --p 8003 --c orange --m "Dit is de vierde server"

python -i portForwarder.py --p 9876
