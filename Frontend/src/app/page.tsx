import Header from "./Header";
import { Analytics } from "@vercel/analytics/react";
import Footer from "./footer";

export default function Home() {
  return (
    <>
      <Analytics /> {/* Use it as a self-closing component */}
      <Header />
      <Footer />
    </>
  );
}