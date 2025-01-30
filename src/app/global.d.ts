// global.d.ts
declare global {
    interface Window {
      gtag: (command: string, eventName: string, params?: Record<string, string | number | boolean | object>) => void;
    }
  }

  export {};
