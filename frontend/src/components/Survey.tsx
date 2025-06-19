import React, { useContext, useEffect } from 'react'

import { useState } from 'react';
import type { SurveyProps, SurveyOption, SurveyStep, InputField } from "../components/interface/interfaces";
import SurveyPageContext from './context/SurveyPageContext';
import { InputTemplates } from './InputTemplates';
import { userAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import "../css/Survey.css"

interface StepData {
    [key: string]: any;
}

const Survey = (props: SurveyProps) => {
    const [savedData, setSavedData] = useState<StepData>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string>('');
    const [refreshing, setRefreshing] = useState(false);
    const [success, setSuccess] = useState<string>('');

    const stepContext = useContext(SurveyPageContext)
    const { refreshUser } = useAuth();

    const first_step = props.steps_total[0].value
    const last_step = props.steps_total[props.steps_total.length - 1].value

    // Определяем, находимся ли мы в режиме редактирования профиля
    const isProfileEditMode = window.location.pathname.includes('/profile/edit');

    // Получаем текущий шаг из контекста
    const currentStepValue = props.steps_total[stepContext.currentStep - 1]?.value || first_step;

    // Загружаем существующие данные профиля при первой загрузке
    // Функция для загрузки существующих данных профиля
    const loadExistingProfileData = async (showRefreshIndicator = false) => {
        try {
            if (showRefreshIndicator) {
                setRefreshing(true);
            }
            
            console.log('🔄 Загружаем данные профиля...');
            const profile = await userAPI.getTrainingProfile();
            console.log('📦 Полученный профиль:', profile);
            
            if (profile?.personal_information || profile?.basic_information) {
                const existingData: StepData = {};
                
                // Загружаем персональную информацию
                if (profile.personal_information) {
                    existingData.name = profile.personal_information.first_name || '';
                    existingData.surname = profile.personal_information.last_name || '';
                    existingData.country = profile.personal_information.country || '';
                    existingData.city = profile.personal_information.city || '';
                    console.log('👤 Персональная информация загружена:', {
                        name: existingData.name,
                        surname: existingData.surname,
                        country: existingData.country,
                        city: existingData.city
                    });
                }
                
                // Загружаем базовую информацию
                if (profile.basic_information) {
                    existingData.gender = profile.basic_information.gender || '';
                    existingData.age = profile.basic_information.age?.toString() || '';
                    existingData.height = profile.basic_information.height_cm?.toString() || '';
                    existingData.weight = profile.basic_information.weight_kg?.toString() || '';
                    console.log('📊 Базовая информация загружена:', {
                        gender: existingData.gender,
                        age: existingData.age,
                        height: existingData.height,
                        weight: existingData.weight,
                        'исходные значения': {
                            age: profile.basic_information.age,
                            height_cm: profile.basic_information.height_cm,
                            weight_kg: profile.basic_information.weight_kg
                        }
                    });
                }

                // Загружаем цели тренировок
                if (profile.training_goals && Array.isArray(profile.training_goals)) {
                    existingData.training_goals = profile.training_goals.join(',');
                }

                // Загружаем опыт тренировок
                if (profile.training_experience) {
                    existingData.training_level = profile.training_experience.level || '';
                    existingData.frequency_last_3_months = profile.training_experience.frequency_last_3_months || '';
                }

                // Загружаем предпочтения
                if (profile.preferences) {
                    existingData.training_location = profile.preferences.training_location || '';
                    existingData.session_duration = profile.preferences.session_duration || '';
                    existingData.location_details = profile.preferences.location_details || '';
                }

                // Загружаем информацию о здоровье
                if (profile.health) {
                    existingData.joint_back_problems = profile.health.joint_back_problems?.toString() || '';
                    existingData.chronic_conditions = profile.health.chronic_conditions?.toString() || '';
                    existingData.health_details = profile.health.health_details || '';
                }

                // Загружаем типы тренировок (рейтинги)
                if (profile.training_types) {
                    existingData.strength_training = profile.training_types.strength_training?.toString() || '';
                    existingData.cardio = profile.training_types.cardio?.toString() || '';
                    existingData.hiit = profile.training_types.hiit?.toString() || '';
                    existingData.yoga_pilates = profile.training_types.yoga_pilates?.toString() || '';
                    existingData.functional_training = profile.training_types.functional_training?.toString() || '';
                    existingData.stretching = profile.training_types.stretching?.toString() || '';
                }
                
                setSavedData(existingData);
                console.log('✅ Данные профиля перезагружены:', existingData);
            } else {
                console.log('⚠️ Профиль пустой или отсутствует');
            }
        } catch (error) {
            console.error('❌ Ошибка загрузки профиля:', error);
            console.log('🆕 Начинаем с пустых данных');
        } finally {
            if (showRefreshIndicator) {
                setRefreshing(false);
            }
        }
    };

    useEffect(() => {
        loadExistingProfileData();
    }, []);

    const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = event.target;
        setSavedData(prev => ({ ...prev, [name]: value }));
        setError(''); // Очищаем ошибку при вводе
        setSuccess(''); // Очищаем сообщение об успехе при вводе
    };

    // Сохранение данных при переходе на следующий шаг
    const saveStepData = async (stepData: StepData) => {
        try {
            setLoading(true);
            setError('');

            // Подготавливаем данные для отправки в зависимости от заполненных полей
            const trainingProfileData: any = {};

            // Персональная информация (только если не пустые)
            if (stepData.name && stepData.name.trim()) trainingProfileData.first_name = stepData.name.trim();
            if (stepData.surname && stepData.surname.trim()) trainingProfileData.last_name = stepData.surname.trim();
            if (stepData.country && stepData.country !== 'select') trainingProfileData.country = stepData.country;
            if (stepData.city && stepData.city.trim()) trainingProfileData.city = stepData.city.trim();

            // Базовая информация (с валидацией)
            if (stepData.gender && stepData.gender !== '') trainingProfileData.gender = stepData.gender;
            
            // Проверяем числовые поля
            console.log('🔢 Обработка числовых полей:', {
                age: stepData.age,
                height: stepData.height,
                weight: stepData.weight
            });
            
            if (stepData.age && stepData.age.trim()) {
                const age = parseInt(stepData.age);
                console.log(`👶 Возраст: "${stepData.age}" → ${age}, валидный: ${!isNaN(age) && age >= 13 && age <= 100}`);
                if (!isNaN(age) && age >= 13 && age <= 100) {
                    trainingProfileData.age = age;
                } else {
                    console.warn(`⚠️ Возраст ${age} не прошел валидацию (должен быть 13-100)`);
                }
            }
            
            if (stepData.height && stepData.height.trim()) {
                const height = parseInt(stepData.height);
                console.log(`📏 Рост: "${stepData.height}" → ${height}, валидный: ${!isNaN(height) && height >= 100 && height <= 250}`);
                if (!isNaN(height) && height >= 100 && height <= 250) {
                    trainingProfileData.height_cm = height;
                } else {
                    console.warn(`⚠️ Рост ${height} не прошел валидацию (должен быть 100-250)`);
                }
            }
            
            if (stepData.weight && stepData.weight.trim()) {
                const weight = parseFloat(stepData.weight);
                console.log(`⚖️ Вес: "${stepData.weight}" → ${weight}, валидный: ${!isNaN(weight) && weight >= 30 && weight <= 300}`);
                if (!isNaN(weight) && weight >= 30 && weight <= 300) {
                    trainingProfileData.weight_kg = weight;
                } else {
                    console.warn(`⚠️ Вес ${weight} не прошел валидацию (должен быть 30-300)`);
                }
            }

            // Дополнительные поля
            if (stepData.training_goals && stepData.training_goals.trim()) {
                trainingProfileData.training_goals = stepData.training_goals.split(',').filter((goal: string) => goal.trim());
            }
            
            if (stepData.training_level && stepData.training_level !== 'select') {
                trainingProfileData.training_level = stepData.training_level;
            }
            
            if (stepData.frequency_last_3_months && stepData.frequency_last_3_months !== 'select') {
                trainingProfileData.frequency_last_3_months = stepData.frequency_last_3_months;
            }
            
            if (stepData.training_location && stepData.training_location !== 'select') {
                trainingProfileData.training_location = stepData.training_location;
            }
            
            if (stepData.session_duration && stepData.session_duration !== 'select') {
                trainingProfileData.session_duration = stepData.session_duration;
            }
            
            if (stepData.location_details && stepData.location_details.trim()) {
                trainingProfileData.location_details = stepData.location_details.trim();
            }
            
            // Boolean поля для здоровья
            if (stepData.joint_back_problems && stepData.joint_back_problems !== '') {
                trainingProfileData.joint_back_problems = stepData.joint_back_problems === 'true';
            }
            
            if (stepData.chronic_conditions && stepData.chronic_conditions !== '') {
                trainingProfileData.chronic_conditions = stepData.chronic_conditions === 'true';
            }
            
            if (stepData.health_details && stepData.health_details.trim()) {
                trainingProfileData.health_details = stepData.health_details.trim();
            }
            
            // Рейтинги тренировок (1-5)
            const trainingTypes = ['strength_training', 'cardio', 'hiit', 'yoga_pilates', 'functional_training', 'stretching'];
            trainingTypes.forEach(type => {
                if (stepData[type] && stepData[type].trim()) {
                    const rating = parseInt(stepData[type]);
                    if (!isNaN(rating) && rating >= 1 && rating <= 5) {
                        trainingProfileData[type] = rating;
                    }
                }
            });

            console.log('Отправляемые данные:', trainingProfileData);

            // Отправляем данные только если есть что сохранить
            if (Object.keys(trainingProfileData).length > 0) {
                await userAPI.updateTrainingProfile(trainingProfileData);
                console.log('Данные успешно сохранены');
                
                // Перезагружаем данные профиля после успешного сохранения
                await loadExistingProfileData(true);
                
                // Обновляем пользователя в AuthContext
                await refreshUser();
                
                setSuccess('Данные успешно сохранены и обновлены!');
                
                // Автоматически скрываем сообщение об успехе через 3 секунды
                setTimeout(() => {
                    setSuccess('');
                }, 3000);
            } else {
                console.log('Нет данных для сохранения');
            }
        } catch (error: any) {
            console.error('Детали ошибки:', error);
            console.error('Ответ сервера:', error.response?.data);
            
            let errorMessage = 'Ошибка при сохранении данных';
            
            if (error.response?.data) {
                if (error.response.data.detail) {
                    if (Array.isArray(error.response.data.detail)) {
                        // Если это массив ошибок валидации Pydantic
                        const validationErrors = error.response.data.detail.map((err: any) => 
                            `${err.loc?.join('.')}: ${err.msg}`
                        ).join(', ');
                        errorMessage = `Ошибки валидации: ${validationErrors}`;
                    } else {
                        errorMessage = error.response.data.detail;
                    }
                } else {
                    errorMessage = JSON.stringify(error.response.data);
                }
            } else {
                errorMessage = error.message;
            }
            
            setError(errorMessage);
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const validateCurrentStep = (): boolean => {
        const currentStepOptions = props.options.find((_, index) => 
            index === stepContext.currentStep - 1
        );
        
        if (!currentStepOptions) return true;
        
        let isValid = true;
        let validationErrors: string[] = [];
        
        currentStepOptions.inputs.forEach(input => {
            const value = savedData[input.name];
            
            if (input.validation) {
                // Проверка обязательных полей
                if (input.validation.required && (!value || value.trim() === '')) {
                    isValid = false;
                    validationErrors.push(`${input.placeholder} is required`);
                    return;
                }
                
                // Проверка числовых полей
                if (input.input_type === "number" && value && value.trim()) {
                    const numValue = parseFloat(value);
                    
                    if (isNaN(numValue)) {
                        isValid = false;
                        validationErrors.push(`${input.placeholder} must be a valid number`);
                    } else {
                        if (input.validation.min !== undefined && numValue < input.validation.min) {
                            isValid = false;
                            validationErrors.push(input.validation.errorMessage || 
                                `${input.placeholder} must be at least ${input.validation.min}`);
                        }
                        if (input.validation.max !== undefined && numValue > input.validation.max) {
                            isValid = false;
                            validationErrors.push(input.validation.errorMessage || 
                                `${input.placeholder} must be at most ${input.validation.max}`);
                        }
                    }
                }
            }
        });
        
        if (!isValid) {
            setError(`Validation errors: ${validationErrors.join(', ')}`);
        }
        
        return isValid;
    };

    const handleContinue = async () => {
        try {
            // Проверяем валидацию перед сохранением
            if (!validateCurrentStep()) {
                return;
            }
            
            await saveStepData(savedData);
            stepContext.updateStep(stepContext.currentStep + 1);
        } catch (error) {
            console.error('Ошибка при сохранении шага:', error);
        }
    };

    const handleBack = () => {
        stepContext.updateStep(stepContext.currentStep - 1);
    };

    const handleSubmit = async () => {
        try {
            // Проверяем валидацию перед финальным сохранением
            if (!validateCurrentStep()) {
                return;
            }
            
            await saveStepData(savedData);
            console.log('Данные опроса сохранены успешно');
            
            if (isProfileEditMode) {
                // В режиме редактирования профиля показываем сообщение об успехе и перезагружаем данные
                setSuccess('Профиль успешно обновлен!');
                await loadExistingProfileData(true);
                setTimeout(() => setSuccess(''), 3000); // Убираем сообщение через 3 секунды
            } else {
                // В режиме первичного заполнения перенаправляем на главную страницу
                window.location.href = '/';
            }
        } catch (error) {
            console.error('Ошибка при финальном сохранении:', error);
        }
    }


    return (
        <div className="survey basic-page">
            <div className="survey__navbar">
                {props.steps_total.map((step: SurveyStep, value: number) => {
                    return (
                        <h3 key={value} className={step.value === currentStepValue ? "survey__navbar__selected" : ""}>
                            {step.placeholder}
                        </h3>
                    )
                })}
            </div>

            <div className="survey__container">
                <div className="survey__options">
                    <div className="survey__title">
                        {props.title}
                    </div>
                    {error && (
                        <div style={{ 
                            color: 'red', 
                            marginBottom: '15px', 
                            padding: '10px', 
                            border: '1px solid red', 
                            borderRadius: '5px',
                            backgroundColor: 'rgba(255, 0, 0, 0.1)'
                        }}>
                            {error}
                        </div>
                    )}
                    {success && (
                        <div style={{ 
                            color: 'green', 
                            marginBottom: '15px', 
                            padding: '10px', 
                            border: '1px solid green', 
                            borderRadius: '5px',
                            backgroundColor: 'rgba(0, 255, 0, 0.1)'
                        }}>
                            {success}
                        </div>
                    )}
                    {(() => {
                        // Показываем только текущую вкладку
                        const currentStepIndex = stepContext.currentStep - 1;
                        const currentStepOption = props.options[currentStepIndex];
                        
                        if (!currentStepOption) return null;
                        
                        return (
                            <div className="survey__options__section">
                                <p>
                                    {currentStepOption.subtitle}
                                </p>
                                <div className="survey__section__forms">
                                    <form>
                                        {currentStepOption.inputs.map((input_option: InputField, value: number) => {
                                            return (
                                                <InputTemplates 
                                                    key={value} 
                                                    {...input_option}
                                                    value={savedData[input_option.name] || ''}
                                                    onChange={handleChange}
                                                />
                                            )
                                        })}
                                    </form>
                                </div>
                            </div>
                        );
                    })()}
                </div>

                <div className="survey__info">
                    <div className="survey__info__description">
                        <div className="survey__title">
                            <h2>
                                {props.information.title}
                            </h2>
                        </div>
                        <p>
                            {props.information.description}
                        </p>
                    </div>
                    <div className="survey__info__button">
                        {
                            currentStepValue !== first_step ?
                                <button className="btn-basic-black" onClick={handleBack} disabled={loading}>
                                    Back
                                </button> : ""
                        }

                        {
                            currentStepValue !== last_step ?
                                <button className="btn-basic-black" onClick={handleContinue} disabled={loading || refreshing}>
                                    {loading ? 'Сохранение...' : refreshing ? 'Обновление...' : 'Continue'}
                                </button> : ""
                        }

                        {
                            currentStepValue === last_step ?
                                <button className="btn-basic-black" onClick={handleSubmit} disabled={loading || refreshing}>
                                    {loading ? 'Сохранение...' : refreshing ? 'Обновление...' : (isProfileEditMode ? 'Save Changes' : 'Submit')}
                                </button> : ""
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Survey