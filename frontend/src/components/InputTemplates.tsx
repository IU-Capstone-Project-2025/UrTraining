// import React from 'react'
import type { InputField, SelectOption } from './interface/interfaces'

export const InputTemplates = (props: InputField) => {
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

export const TextInputTemplate = (props: InputField) => {
    return (
        <input
            type={props.input_type}
            id={props.id}
            name={props.name}
            className="form-basic-white"
            placeholder={props.placeholder}
        />
    )
}

export const SelectInputTemplate = (props: InputField) => {
    return (
        <select
            id={props.id}
            name={props.name}
            className="form-basic-white"
            defaultValue={"select"}
        >
            <option disabled value={"select"}>Country... </option>
            {props.options === "" ? [] : props.options.map((option: SelectOption, value: number) => {
                return (
                    <option key={value} value={option.value}>
                        {option.placeholder}
                    </option>
                )
            })}
        </select>
    )
}

export const RadioInputTemplate = (props: InputField) => {
    return (
        <>
            {(props.options === "" ? [] : props.options).map((option: SelectOption, value: number) => {
                return (
                    <label key={value} className="radio-basic-black">
                        <input
                            type={props.input_type}
                            id={option.id}
                            name={option.name}
                            value={option.value}
                        />
                        <div>{option.placeholder}</div>
                    </label>
                )
            })}
        </>
    )
}

export const ScaleInputTemplate = (props: InputField) => {
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
                        />
                        <span>{num}</span>
                    </label>
                ))}
            </div>
        </div>
    )
}

export default InputTemplates