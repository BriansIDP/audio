#pragma once
#include <torch/torch.h>
#include <torchaudio/csrc/ffmpeg/ffmpeg.h>
#include <torchaudio/csrc/ffmpeg/stream_reader/typedefs.h>

namespace torchaudio {
namespace io {

//////////////////////////////////////////////////////////////////////////////
// Buffer Interface
//////////////////////////////////////////////////////////////////////////////
class Buffer {
 public:
  virtual ~Buffer() = default;

  //////////////////////////////////////////////////////////////////////////////
  // Query
  //////////////////////////////////////////////////////////////////////////////
  // Check if buffeer has enoough number of frames for a chunk
  virtual bool is_ready() const = 0;

  //////////////////////////////////////////////////////////////////////////////
  // Modifiers
  //////////////////////////////////////////////////////////////////////////////
  virtual void push_frame(AVFrame* frame, double pts) = 0;

  virtual c10::optional<Chunk> pop_chunk() = 0;

  virtual void flush() = 0;
};

} // namespace io
} // namespace torchaudio
