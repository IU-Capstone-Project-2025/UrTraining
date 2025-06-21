import React, { useState } from 'react'
import type { InputField, SelectOption } from './interface/interfaces'

export const InputTemplates = (props: InputField) => {
    if (props.input_type === "text" ||
        props.input_type === "number")
        return <TextInputTemplate {...props} />
    if (props.input_type === "textarea")
        return <TextAreaTemplate {...props} />
    if (props.input_type === "select")
        return <SelectInputTemplate {...props} />
    if (props.input_type === "radio")
        return <RadioInputTemplate {...props} />
<<<<<<< HEAD
    if (props.input_type === "checkbox")
        return <CheckboxInputTemplate {...props} />
    if (props.input_type === "rating")
        return <RatingInputTemplate {...props} />
=======
    if (props.input_type === "scale")
    return <ScaleInputTemplate {...props} />    
>>>>>>> 3d1ddfca2fd1740408c2b69c66f7147958f4de1f

    return (
        <div>
            No suitable template
        </div>
    )
}

export const TextInputTemplate = (props: InputField) => {
    const [error, setError] = useState<string>('');

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event.target.value;
        
        // Валидация для числовых полей
        if (props.input_type === "number" && props.validation) {
            const numValue = parseFloat(value);
            
            if (value && !isNaN(numValue)) {
                if (props.validation.min !== undefined && numValue < props.validation.min) {
                    setError(props.validation.errorMessage || `Minimum value is ${props.validation.min}`);
                } else if (props.validation.max !== undefined && numValue > props.validation.max) {
                    setError(props.validation.errorMessage || `Maximum value is ${props.validation.max}`);
                } else {
                    setError('');
                }
            } else if (value && isNaN(numValue)) {
                setError('Please enter a valid number');
            } else {
                setError('');
            }
        }
        
        // Вызываем родительский onChange
        if (props.onChange) {
            props.onChange(event);
        }
    };

    return (
        <div>
            {props.label && (
                <label htmlFor={props.id} style={{
                    display: 'block',
                    marginBottom: '5px',
                    fontWeight: '500',
                    color: '#333'
                }}>
                    {props.label}
                    {props.validation?.required && <span style={{ color: 'red' }}> *</span>}
                </label>
            )}
            <input
                type={props.input_type}
                id={props.id}
                name={props.name}
                className={`form-basic-white ${error ? 'error' : ''}`}
                placeholder={props.placeholder}
                value={props.value || ''}
                onChange={handleChange}
                min={props.validation?.min}
                max={props.validation?.max}
            />
            {error && (
                <div style={{
                    color: 'red',
                    fontSize: '12px',
                    marginTop: '5px',
                    padding: '2px 5px',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    borderRadius: '3px',
                    border: '1px solid rgba(255, 0, 0, 0.3)'
                }}>
                    {error}
                </div>
            )}
        </div>
    )
}

export const SelectInputTemplate = (props: InputField) => {
    return (
<<<<<<< HEAD
        <div>
            {props.label && (
                <label htmlFor={props.id} style={{
                    display: 'block',
                    marginBottom: '5px',
                    fontWeight: '500',
                    color: '#333'
                }}>
                    {props.label}
                    {props.validation?.required && <span style={{ color: 'red' }}> *</span>}
                </label>
            )}
            <select
                id={props.id}
                name={props.name}
                className="form-basic-white"
                value={props.value || ""}
                onChange={props.onChange}
            >
                {/* Показываем placeholder только если нет опции "Не выбрано" */}
                {!(props.options !== "" && props.options.some((option: any) => option.value === "")) && (
                    <option disabled value="">
                        {props.placeholder}
=======
        <select
            id={props.id}
            name={props.name}
            className="form-basic-white"
            defaultValue={"select"}
        >
            <option disabled value={"select"}>Select... </option>
            {props.options === "" ? [] : props.options.map((option: SelectOption, value: number) => {
                return (
                    <option key={value} value={option.value}>
                        {option.placeholder}
>>>>>>> 3d1ddfca2fd1740408c2b69c66f7147958f4de1f
                    </option>
                )}
                {props.options === "" ? [] : props.options.map((option: SelectOption, index: number) => {
                    return (
                        <option key={index} value={option.value}>
                            {option.placeholder}
                        </option>
                    )
                })}
            </select>
        </div>
    )
}

export const RadioInputTemplate = (props: InputField) => {
    return (
        <div>
            {props.label && (
                <label style={{
                    display: 'block',
                    marginBottom: '10px',
                    fontWeight: '500',
                    color: '#333'
                }}>
                    {props.label}
                    {props.validation?.required && <span style={{ color: 'red' }}> *</span>}
                </label>
            )}
            {(props.options === "" ? [] : props.options).map((option: SelectOption, value: number) => {
                return (
                    <label key={value} className="radio-basic-black">
                        <input
                            type={props.input_type}
                            id={option.id}
                            name={props.name}
                            value={option.value}
                            checked={props.value === option.value}
                            onChange={props.onChange}
                        />
                        <div>{option.placeholder}</div>
                    </label>
                )
            })}
        </div>
    )
}

export const TextAreaTemplate = (props: InputField) => {
    return (
        <div>
            {props.label && (
                <label htmlFor={props.id} style={{
                    display: 'block',
                    marginBottom: '5px',
                    fontWeight: '500',
                    color: '#333'
                }}>
                    {props.label}
                    {props.validation?.required && <span style={{ color: 'red' }}> *</span>}
                </label>
            )}
            <textarea
                id={props.id}
                name={props.name}
                className="form-basic-white"
                placeholder={props.placeholder}
                value={props.value || ''}
                onChange={props.onChange}
                rows={3}
                style={{ resize: 'vertical', minHeight: '80px' }}
            />
        </div>
    )
}

export const CheckboxInputTemplate = (props: InputField) => {
    // Для множественного выбора, значение хранится как строка с разделителями
    const selectedValues = props.value ? props.value.split(',') : [];
    
    const handleCheckboxChange = (optionValue: string, checked: boolean) => {
        let newValues = [...selectedValues];
        
        if (checked) {
            if (!newValues.includes(optionValue)) {
                newValues.push(optionValue);
            }
        } else {
            newValues = newValues.filter(val => val !== optionValue);
        }
        
        // Создаем событие для совместимости с onChange
        const syntheticEvent = {
            target: {
                name: props.name,
                value: newValues.join(',')
            }
        } as React.ChangeEvent<HTMLInputElement>;
        
        if (props.onChange) {
            props.onChange(syntheticEvent);
        }
    };

    return (
        <div>
            {props.label && (
                <label style={{
                    display: 'block',
                    marginBottom: '10px',
                    fontWeight: '500',
                    color: '#333'
                }}>
                    {props.label}
                    {props.validation?.required && <span style={{ color: 'red' }}> *</span>}
                </label>
            )}
            {(props.options === "" ? [] : props.options).map((option: SelectOption, index: number) => {
                const isChecked = selectedValues.includes(option.value);
                return (
                    <label key={index} className="checkbox-basic" style={{ display: 'block', marginBottom: '8px' }}>
                        <input
                            type="checkbox"
                            id={option.id}
                            name={`${props.name}_${option.value}`}
                            value={option.value}
                            checked={isChecked}
                            onChange={(e) => handleCheckboxChange(option.value, e.target.checked)}
                            style={{ marginRight: '8px' }}
                        />
                        <span>{option.placeholder}</span>
                    </label>
                )
            })}
        </div>
    )
}

export const RatingInputTemplate = (props: InputField) => {
    const [error, setError] = useState<string>('');
    const rating = parseInt(props.value || '0');

    const handleRatingClick = (value: number) => {
        // Создаем событие для совместимости с onChange
        const syntheticEvent = {
            target: {
                name: props.name,
                value: value.toString()
            }
        } as React.ChangeEvent<HTMLInputElement>;
        
        if (props.onChange) {
            props.onChange(syntheticEvent);
        }
    };

    return (
        <div>
            {props.label && (
                <label style={{
                    display: 'block',
                    marginBottom: '10px',
                    fontWeight: '500',
                    color: '#333'
                }}>
                    {props.label}
                    {props.validation?.required && <span style={{ color: 'red' }}> *</span>}
                </label>
            )}
            <div style={{ display: 'flex', gap: '5px', alignItems: 'center' }}>
                {[1, 2, 3, 4, 5].map((star) => (
                    <button
                        key={star}
                        type="button"
                        onClick={() => handleRatingClick(star)}
                        style={{
                            background: 'none',
                            border: 'none',
                            fontSize: '24px',
                            cursor: 'pointer',
                            color: star <= rating ? '#FFD700' : '#DDD',
                            padding: '5px'
                        }}
                    >
                        ★
                    </button>
                ))}
                <span style={{ marginLeft: '10px', fontSize: '14px', color: '#666' }}>
                    {rating > 0 ? `${rating}/5` : 'Not rated'}
                </span>
            </div>
            {error && (
                <div style={{
                    color: 'red',
                    fontSize: '12px',
                    marginTop: '5px',
                    padding: '2px 5px',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    borderRadius: '3px',
                    border: '1px solid rgba(255, 0, 0, 0.3)'
                }}>
                    {error}
                </div>
            )}
        </div>
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