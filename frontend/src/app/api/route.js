import { NextResponse } from 'next/server';

export async function POST(req) {
  try {
    const body = await req.json();

    // Use BACKEND_URL in prod; fall back to local in dev
    const base = (process.env.BACKEND_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

    const r = await fetch(`${base}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const contentType = r.headers.get('content-type') || 'application/json';
    const text = await r.text(); // pass through whatever the backend returns

    return new NextResponse(text, {
      status: r.status,
      headers: { 'Content-Type': contentType },
    });
  } catch (err) {
    return new NextResponse(
      JSON.stringify({ error: 'Proxy to backend failed', details: String(err) }),
      { status: 502, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

// Optional: simple health check
export async function GET() {
  return NextResponse.json({ ok: true });
}
