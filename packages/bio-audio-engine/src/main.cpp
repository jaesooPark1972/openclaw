#include "BioAcousticParams.h"
#include <cmath>
#include <iostream>
#include <napi.h>
#include <vector>


// Example: Simple "Bio-Check" function exposed to JS
// Returns true if the frequency is within human vocal range
Napi::Boolean CheckVocalPlausibility(const Napi::CallbackInfo &info) {
  Napi::Env env = info.Env();

  if (info.Length() < 1 || !info[0].IsNumber()) {
    Napi::TypeError::New(env, "Number expected (Frequency in Hz)")
        .ThrowAsJavaScriptException();
    return Napi::Boolean::New(env, false);
  }

  double frequency = info[0].As<Napi::Number>().DoubleValue();

  bool isPlausible =
      (frequency >= BioAcoustic::VocalConstraints::MIN_HUMAN_FUNDAMENTAL_FREQ &&
       frequency <= BioAcoustic::VocalConstraints::MAX_HUMAN_FUNDAMENTAL_FREQ);

  return Napi::Boolean::New(env, isPlausible);
}

// Example: Placeholder for heavy DSP processing
Napi::String ProcessAudioStem(const Napi::CallbackInfo &info) {
  Napi::Env env = info.Env();
  // In real implementation, this would take a buffer and process it
  return Napi::String::New(
      env, "Bio-Acoustic Engine v0.1: Ready for Quantum Processing");
}

// Initialize the Addon
Napi::Object Init(Napi::Env env, Napi::Object exports) {
  exports.Set(Napi::String::New(env, "checkVocalPlausibility"),
              Napi::Function::New(env, CheckVocalPlausibility));
  exports.Set(Napi::String::New(env, "processAudio"),
              Napi::Function::New(env, ProcessAudioStem));

  return exports;
}

NODE_API_MODULE(bio_audio_engine, Init)
