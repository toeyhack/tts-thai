from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import VitsTokenizer, VitsModel
import torch
import soundfile as sf
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

# โหลดโมเดลครั้งเดียวตอนเริ่มต้น
male_model = VitsModel.from_pretrained("VIZINTZOR/MMS-TTS-THAI-MALEV2")
male_tokenizer = VitsTokenizer.from_pretrained("VIZINTZOR/MMS-TTS-THAI-MALEV2")

female_model = VitsModel.from_pretrained("VIZINTZOR/MMS-TTS-THAI-FEMALEV2")
female_tokenizer = VitsTokenizer.from_pretrained("VIZINTZOR/MMS-TTS-THAI-FEMALEV2")

class TTSRequest(BaseModel):
    text: str
    voice: str  # male หรือ female

def synthesize_speech(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        speech = model(**inputs).waveform
    sr = model.config.sampling_rate if hasattr(model.config, "sampling_rate") else 22050
    buffer = io.BytesIO()
    sf.write(buffer, speech.squeeze().numpy(), sr, format="wav")
    buffer.seek(0)
    return buffer

@app.post("/tts/")
async def tts_endpoint(request: TTSRequest):
    if request.voice == "male":
        buffer = synthesize_speech(male_model, male_tokenizer, request.text)
    elif request.voice == "female":
        buffer = synthesize_speech(female_model, female_tokenizer, request.text)
    else:
        raise HTTPException(status_code=400, detail="voice must be 'male' or 'female'")
    return StreamingResponse(buffer, media_type="audio/wav", headers={
        "Content-Disposition": f"attachment; filename={request.voice}_output.wav"
    })
