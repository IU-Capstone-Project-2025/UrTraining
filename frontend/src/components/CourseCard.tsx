import star from '../assets/star.svg';

interface CourseCardProps {
  course_info: any;
  header_badges: any;
  progressPercentage?: number;
  isSaved?: boolean;
}

const CourseCard = (data: CourseCardProps) => {
  return (
    <div className='catalogue__course__card'>
        <div className='catalogue__course__tags'>
            {Object.entries(data.header_badges).map(([sectionKey, badges]: any) => (
            <div 
                key={sectionKey} 
                className="catalogue__tags__category"
            >
                {badges.map((badge: any, idx: any) => (
                    <div
                        key={idx}
                        className="catalogue__tag"
                        style={{ 
                            boxShadow: `inset 0px 0px 0px 1.5px ${badge.badge_color}`, color: badge.badge_color}}
                    >
                {badge.badge_text}
              </div>
            ))}
          </div>
        ))}
      </div>

      <div className='catalogue__course__title'>
            <h2>{data.course_info.title}</h2>
            <p>by {data.course_info.author}</p>
      </div>

      <div className='catalogue__course__rating'>
          <img src={star} alt="Rating"/>
          <span>
            {data.course_info.rating.toFixed(1)}/5.0 
          </span>
          <span>
             ({data.course_info.reviews} reviews)
          </span>
      </div>

      {/* Progress indicator - only show if training is saved */}
      {data.isSaved && typeof data.progressPercentage === 'number' && (
        <div className='catalogue__course__progress'>
          <span>Progress: {data.progressPercentage.toFixed(0)}%</span>
        </div>
      )}
    </div>
  );
};

export default CourseCard;