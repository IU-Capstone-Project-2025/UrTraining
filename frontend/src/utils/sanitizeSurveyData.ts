import type { InputField, InputType, SurveyProps } from "../components/interface/interfaces";

const validInputTypes: InputType[] = ["text", "number", "email", "password", "select", "radio", "scale"];

function sanitizeInputField(field: any): InputField {
  return {
    name: field.name,
    id: field.id,
    input_type: validInputTypes.includes(field.input_type) ? field.input_type : "text",
    placeholder: field.placeholder || "",
    options: Array.isArray(field.options) ? field.options : ""
  };
}

export function sanitizeSurveyData(raw: any): SurveyProps {
  return {
    steps_total: raw.steps_total,
    step_current: raw.step_current,
    title: raw.title,
    information: raw.information,
    options: raw.options.map((opt: any) => ({
      subtitle: opt.subtitle,
      inputs: opt.inputs.map((inp: any) => sanitizeInputField(inp))
    }))
  };
}
