// import React from 'react'
import type { InputField, SelectOption } from './interface/interfaces'

interface ControlledInputField extends InputField {
    value: any;
    onChange: (e: React.ChangeEvent<any>) => void;
}

export const InputTemplates = (props: ControlledInputField) => {
    if (props.input_type === "text" ||
        props.input_type === "number")
        return <TextInputTemplate {...props} />
    if (props.input_type === "select")
        return <SelectInputTemplate {...props} />
    if (props.input_type === "radio")
        return <RadioInputTemplate {...props} />
    if (props.input_type === "scale")
    return <ScaleInputTemplate {...props} />    

    return (
        <div>
            No suitable template
        </div>
    )
}

export const TextInputTemplate = (props: ControlledInputField) => {
    return (
        <input
            type={props.input_type}
            id={props.id}
            name={props.name}
            className="form-basic-white"
            placeholder={props.placeholder}
            value={props.value || ""}
            onChange={props.onChange}
        />
    )
}

export const SelectInputTemplate = (props: ControlledInputField) => {
    return (
        <select
            id={props.id}
            name={props.name}
            className="form-basic-white"
            value={props.value || "select"}
            onChange={props.onChange}
        >
            <option disabled value={"select"}>Select... </option>
            {props.options?.map((option: SelectOption, index: number) => (
                <option key={index} value={option.value}>
                    {option.placeholder}
                </option>
            ))}
        </select>
    )
}

export const RadioInputTemplate = (props: ControlledInputField) => {
    return (
        <>
            {(props.options.length === 0 ? [] : props.options).map((option: SelectOption, value: number) => {
                return (
                    <label key={value} className="radio-basic-black">
                        <input
                            type={props.input_type}
                            id={option.id}
                            name={option.name}
                            value={option.value}
                            checked={props.value === option.value}
                            onChange={props.onChange}
                        />
                        <div>{option.placeholder}</div>
                    </label>
                )
            })}
        </>
    )
}

export const ScaleInputTemplate = (props: ControlledInputField) => {
    return (
        <div className="scale-input-row">
            <label className="scale-label">{props.placeholder}</label>
            <div className="scale-options">
                {[1, 2, 3, 4, 5].map((num) => (
                    <label key={num} className="scale-option">
                        <input
                            type="radio"
                            name={props.name}
                            value={num}
                            checked={props.value === String(num)}
                            onChange={props.onChange}
                        />
                        <span>{num}</span>
                    </label>
                ))}
            </div>
        </div>
    )
}


export default InputTemplates