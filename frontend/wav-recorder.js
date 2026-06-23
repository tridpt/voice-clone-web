// WavRecorder: thu âm từ micro và encode thành WAV 16-bit PCM mono.
// Dùng WAV (không phải webm) vì pipeline fine-tune cần định dạng này.

class WavRecorder {
  constructor(targetSampleRate = 22050) {
    this.targetSampleRate = targetSampleRate;
    this.audioContext = null;
    this.mediaStream = null;
    this.processor = null;
    this.source = null;
    this.chunks = [];
    this.recording = false;
  }

  async start() {
    this.mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true },
    });
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.source = this.audioContext.createMediaStreamSource(this.mediaStream);

    // ScriptProcessor đơn giản, tương thích rộng
    this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
    this.chunks = [];
    this.recording = true;

    this.processor.onaudioprocess = (e) => {
      if (!this.recording) return;
      // copy dữ liệu kênh trái
      this.chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
    };

    this.source.connect(this.processor);
    this.processor.connect(this.audioContext.destination);
  }

  stop() {
    this.recording = false;
    const sampleRate = this.audioContext ? this.audioContext.sampleRate : 44100;

    if (this.processor) this.processor.disconnect();
    if (this.source) this.source.disconnect();
    if (this.mediaStream) this.mediaStream.getTracks().forEach((t) => t.stop());
    if (this.audioContext) this.audioContext.close();

    const merged = this._merge(this.chunks);
    const down = this._downsample(merged, sampleRate, this.targetSampleRate);
    return this._encodeWav(down, this.targetSampleRate);
  }

  _merge(chunks) {
    const length = chunks.reduce((sum, c) => sum + c.length, 0);
    const result = new Float32Array(length);
    let offset = 0;
    for (const c of chunks) {
      result.set(c, offset);
      offset += c.length;
    }
    return result;
  }

  _downsample(buffer, inRate, outRate) {
    if (outRate >= inRate) return buffer;
    const ratio = inRate / outRate;
    const newLen = Math.round(buffer.length / ratio);
    const result = new Float32Array(newLen);
    let pos = 0;
    let bufPos = 0;
    while (pos < newLen) {
      const next = Math.round((pos + 1) * ratio);
      let sum = 0;
      let count = 0;
      for (let i = bufPos; i < next && i < buffer.length; i++) {
        sum += buffer[i];
        count++;
      }
      result[pos] = count > 0 ? sum / count : 0;
      pos++;
      bufPos = next;
    }
    return result;
  }

  _encodeWav(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);
    const writeStr = (offset, str) => {
      for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
    };

    writeStr(0, "RIFF");
    view.setUint32(4, 36 + samples.length * 2, true);
    writeStr(8, "WAVE");
    writeStr(12, "fmt ");
    view.setUint32(16, 16, true);      // PCM chunk size
    view.setUint16(20, 1, true);       // format = PCM
    view.setUint16(22, 1, true);       // mono
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true); // byte rate
    view.setUint16(32, 2, true);       // block align
    view.setUint16(34, 16, true);      // bits per sample
    writeStr(36, "data");
    view.setUint32(40, samples.length * 2, true);

    let offset = 44;
    for (let i = 0; i < samples.length; i++) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
      offset += 2;
    }
    return new Blob([view], { type: "audio/wav" });
  }
}

window.WavRecorder = WavRecorder;
