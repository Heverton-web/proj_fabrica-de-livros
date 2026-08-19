interface InferenceRequest {
  model?: string;
  messages: Array<{ role: string; content: string }>;
  stream?: boolean;
}

const DEFAULT_MODEL = "@cf/meta/llama-3.1-8b-instruct";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    // GET / — model list
    if (url.pathname === "/" && request.method === "GET") {
      return Response.json({
        endpoint: "/inference",
        default_model: DEFAULT_MODEL,
        models: {
          chat: "@cf/meta/llama-3.1-8b-instruct",
          chat_large: "@cf/meta/llama-3.1-70b-instruct",
          coding: "@cf/moonshotai/kimi-k2.7-code",
          embedding: "@cf/baai/bge-base-en-v1.5",
          image: "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        },
      });
    }

    // POST /inference — run model
    if (url.pathname === "/inference" && request.method === "POST") {
      const body = (await request.json()) as InferenceRequest;

      if (!body.messages?.length) {
        return Response.json({ error: "messages[] required" }, { status: 400 });
      }

      const model = body.model || DEFAULT_MODEL;

      try {
        const result = await env.AI.run(model, {
          messages: body.messages,
          stream: body.stream ?? false,
        });

        return Response.json(result, {
          headers: { "Access-Control-Allow-Origin": "*" },
        });
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : "AI inference failed";
        return Response.json(
          { error: msg },
          { status: 500 }
        );
      }
    }

    return Response.json({ error: "Not found" }, { status: 404 });
  },
};
