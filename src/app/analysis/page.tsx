import { Suspense } from "react";
import AnalysisPage from "./analysispage";

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <AnalysisPage />
    </Suspense>
  );
}
