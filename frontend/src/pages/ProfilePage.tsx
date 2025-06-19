import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { userAPI } from '../services/api'

// Страница просмотра профиля пользователя, которая отображает все данные тренировочного профиля в структурированном виде.
// Страница загружает данные профиля через API, показывает основную информацию пользователя (username, email), персональную информацию (имя, фамилия, страна, город),
// физические данные (пол, возраст, рост, вес), цели тренировок, предпочтения, информацию о здоровье и интерес к различным типам тренировок с рейтингами от 1 до 5,
// а также предоставляет кнопку "Редактировать профиль" для перехода к ProfileEditPage.
// Очевидно, что это dummy-страница, которая используется лишь временно

const ProfilePage = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const profileData = await userAPI.getTrainingProfile();
      setProfile(profileData);
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error);
      setError('Не удалось загрузить профиль');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <h2>Загрузка профиля...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <h2>Ошибка</h2>
        <p>{error}</p>
        <Link to="/profile/edit">
          <button className="btn-basic-black">Создать профиль</button>
        </Link>
      </div>
    );
  }

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '30px'
      }}>
        <h1>Мой профиль</h1>
        <Link to="/profile/edit">
          <button className="btn-basic-black">Редактировать профиль</button>
        </Link>
      </div>

      {/* Основная информация */}
      <div style={{ marginBottom: '30px' }}>
        <h2>Основная информация</h2>
        <div style={{ 
          backgroundColor: '#f8f9fa', 
          padding: '20px', 
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          <p><strong>Имя пользователя:</strong> {user?.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Полное имя:</strong> {user?.full_name || 'Не указано'}</p>
        </div>
      </div>

      {profile && (
        <>
          {/* Персональная информация */}
          {profile.personal_information && (
            <div style={{ marginBottom: '30px' }}>
              <h2>Персональная информация</h2>
              <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '20px', 
                borderRadius: '8px',
                marginBottom: '20px'
              }}>
                <p><strong>Имя:</strong> {profile.personal_information.first_name || 'Не указано'}</p>
                <p><strong>Фамилия:</strong> {profile.personal_information.last_name || 'Не указано'}</p>
                <p><strong>Страна:</strong> {profile.personal_information.country || 'Не указано'}</p>
                <p><strong>Город:</strong> {profile.personal_information.city || 'Не указано'}</p>
              </div>
            </div>
          )}

          {/* Физические данные */}
          {profile.basic_information && (
            <div style={{ marginBottom: '30px' }}>
              <h2>Физические данные</h2>
              <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '20px', 
                borderRadius: '8px',
                marginBottom: '20px'
              }}>
                <p><strong>Пол:</strong> {profile.basic_information.gender || 'Не указано'}</p>
                <p><strong>Возраст:</strong> {profile.basic_information.age || 'Не указано'}</p>
                <p><strong>Рост:</strong> {profile.basic_information.height_cm ? `${profile.basic_information.height_cm} см` : 'Не указано'}</p>
                <p><strong>Вес:</strong> {profile.basic_information.weight_kg ? `${profile.basic_information.weight_kg} кг` : 'Не указано'}</p>
              </div>
            </div>
          )}

          {/* Цели тренировок */}
          {profile.training_goals && profile.training_goals.length > 0 && (
            <div style={{ marginBottom: '30px' }}>
              <h2>Цели тренировок</h2>
              <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '20px', 
                borderRadius: '8px',
                marginBottom: '20px'
              }}>
                <ul>
                  {profile.training_goals.map((goal: string, index: number) => (
                    <li key={index}>{goal}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Предпочтения */}
          {profile.preferences && (
            <div style={{ marginBottom: '30px' }}>
              <h2>Предпочтения тренировок</h2>
              <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '20px', 
                borderRadius: '8px',
                marginBottom: '20px'
              }}>
                <p><strong>Место тренировок:</strong> {profile.preferences.training_location || 'Не указано'}</p>
                <p><strong>Продолжительность сессии:</strong> {profile.preferences.session_duration || 'Не указано'}</p>
                {profile.preferences.location_details && (
                  <p><strong>Дополнительные детали:</strong> {profile.preferences.location_details}</p>
                )}
              </div>
            </div>
          )}

          {/* Здоровье */}
          {profile.health && (
            <div style={{ marginBottom: '30px' }}>
              <h2>Информация о здоровье</h2>
              <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '20px', 
                borderRadius: '8px',
                marginBottom: '20px'
              }}>
                <p><strong>Проблемы с суставами/спиной:</strong> {profile.health.joint_back_problems ? 'Да' : 'Нет'}</p>
                <p><strong>Хронические заболевания:</strong> {profile.health.chronic_conditions ? 'Да' : 'Нет'}</p>
                {profile.health.health_details && (
                  <p><strong>Дополнительная информация:</strong> {profile.health.health_details}</p>
                )}
              </div>
            </div>
          )}

          {/* Типы тренировок */}
          {profile.training_types && (
            <div style={{ marginBottom: '30px' }}>
              <h2>Интерес к типам тренировок</h2>
              <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '20px', 
                borderRadius: '8px',
                marginBottom: '20px'
              }}>
                <p><strong>Силовые тренировки:</strong> {profile.training_types.strength_training ? `${profile.training_types.strength_training}/5` : 'Не указано'}</p>
                <p><strong>Кардио:</strong> {profile.training_types.cardio ? `${profile.training_types.cardio}/5` : 'Не указано'}</p>
                <p><strong>HIIT:</strong> {profile.training_types.hiit ? `${profile.training_types.hiit}/5` : 'Не указано'}</p>
                <p><strong>Йога/Пилатес:</strong> {profile.training_types.yoga_pilates ? `${profile.training_types.yoga_pilates}/5` : 'Не указано'}</p>
                <p><strong>Функциональные тренировки:</strong> {profile.training_types.functional_training ? `${profile.training_types.functional_training}/5` : 'Не указано'}</p>
                <p><strong>Растяжка:</strong> {profile.training_types.stretching ? `${profile.training_types.stretching}/5` : 'Не указано'}</p>
              </div>
            </div>
          )}
        </>
      )}

      {!profile && (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <h2>Профиль не заполнен</h2>
          <p>Заполните профиль, чтобы получить персонализированные рекомендации</p>
          <Link to="/profile/edit">
            <button className="btn-basic-black">Заполнить профиль</button>
          </Link>
        </div>
      )}
    </div>
  )
}

export default ProfilePage 