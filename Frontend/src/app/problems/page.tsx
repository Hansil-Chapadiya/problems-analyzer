import { Suspense } from "react";
import ClassifyPage from "./classifypage";

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <ClassifyPage />
    </Suspense>
  );
}
