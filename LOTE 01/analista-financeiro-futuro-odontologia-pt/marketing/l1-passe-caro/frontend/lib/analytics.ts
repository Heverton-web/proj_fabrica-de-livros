export function trackEvent(eventName: string, params?: Record<string, string>) {
  if (typeof window === "undefined") return;

  // Google Analytics 4
  if (window.gtag) {
    window.gtag("event", eventName, params);
  }

  // Log para debug em desenvolvimento
  if (process.env.NODE_ENV === "development") {
    console.log("[Analytics]", eventName, params);
  }
}

export function trackPageView(url: string) {
  trackEvent("page_view", { page_location: url });
}

export function trackLeadCapture(email: string) {
  trackEvent("generate_lead", {
    currency: "BRL",
    value: "0",
    email,
  });
}

export function trackPurchase(value: number) {
  trackEvent("purchase", {
    currency: "BRL",
    value: value.toString(),
  });
}

export function trackBeginCheckout(value: number) {
  trackEvent("begin_checkout", {
    currency: "BRL",
    value: value.toString(),
  });
}

// Tipagem global para gtag
declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
  }
}
