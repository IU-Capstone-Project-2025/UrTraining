import { Link } from 'react-router-dom';
import star from '../assets/star.svg';
import "../css/CoursesCatalogue.css";

const CourseCard = (data: any) => {
  return (
    <Link 
        to={`/course/${data.id}`}
        className="course-card"
    >
        <div className='course-tags-container'>
            {Object.entries(data.header_badges).map(([sectionKey, badges]: any) => (
            <div 
                key={sectionKey} 
                className="badges-group"
            >
                {badges.map((badge: any, idx: any) => (
                    <div
                        key={idx}
                        className="badge"
                        style={{ 
                            boxShadow: `inset 0px 0px 0px 1.5px ${badge.badge_color}`, color: badge.badge_color}}
                    >
                {badge.badge_text}
              </div>
            ))}
          </div>
        ))}
      </div>

      <div className='course__info flex-grow'>
        <div className='course__info__title mb-4'>
          <div className='course__info__text'>
            <h2 className='course__info__name text-xl font-bold mb-1'>{data.course_info.title}</h2>
            <h3 className='course__info__author text-gray-500'>by {data.course_info.author}</h3>
          </div>
        </div>
      </div>

      <div className='course__info__reviews flex justify-between items-center mt-auto'>
        <div className="flex items-center gap-1">
          <img src={star} alt="Rating" className="w-4 h-4" />
          <span className="text-sm font-medium">
            {data.course_info.rating.toFixed(1)}/5 
          </span>
          <span className="text-gray-400 text-xs">
             ({data.course_info.reviews} reviews)
          </span>
        </div>
      </div>
    </Link>
  );
};

export default CourseCard;