import { useState } from 'react';

function App() {
  const [text, setText] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setVideoUrl('');
    if (!text.trim()) {
      setError('Please enter some text');
      return;
    }

    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/generatevideo/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Error generating video');
      }

      // Django returns something like /media/video/<id>.mp4
      const absoluteUrl = `http://127.0.0.1:8000${data.video_url}`;
      setVideoUrl(absoluteUrl);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '700px', margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>Text → Talking Avatar Video</h1>
      <p>Type text and get a video where the avatar speaks it</p>

      <form onSubmit={handleSubmit}>
        <textarea
          rows={4}
          style={{ width: '100%', marginBottom: '12px' }}
          placeholder="Type what you want the avatar to say..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Video'}
        </button>
      </form>

      {error && (
        <div style={{ color: 'red', marginTop: '12px' }}>
          {error}
        </div>
      )}

      {videoUrl && (
        <div style={{ marginTop: '24px' }}>
          <h2>Your Video</h2>
          <video
            src={videoUrl}
            controls
            style={{ width: '100%', borderRadius: '8px' }}
          />
          <p>
            <a href={videoUrl} download>
              Download video
            </a>
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
