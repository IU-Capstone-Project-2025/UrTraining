import React, { createContext } from "react";

interface MetadataContextType {
  savedData: any;
  setSavedData: (metadata: any) => void;
}

export const MetadataContext = createContext<MetadataContextType>({
  savedData: "",
  setSavedData: () => {}
});

export default MetadataContext;