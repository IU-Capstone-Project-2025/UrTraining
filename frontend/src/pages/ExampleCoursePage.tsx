// import React from 'react'
import Course from "../components/Course"
import kanye from '../assets/kanye.jpg'

const ExampleCoursePage = () => {

    const training_data = {
        header_badges: {
            training_type: [
                {
                    badge_text: "Mobility",
                    badge_color: "#9747FF"
                }
            ],
            training_info: [
                {
                    badge_text: "for all levels",
                    badge_color: "#696969"
                },
                {
                    badge_text: "30 min/training",
                    badge_color: "#696969"
                },
                {
                    badge_text: "3-4 trainings/week",
                    badge_color: "#696969"
                },
                {
                    badge_text: "2 weeks",
                    badge_color: "#696969"
                },
            ],
            training_equipment: [
                {
                    badge_text: "No equipment",
                    badge_color: "#888EE3"
                }
            ],
        },
        course_info: {
            title: "Mobility reset",
            author: "trainerOne",
            description: `A short but effective mobility reboot.
                    This program is designed to help you restore natural joint range of motion,
                    improve flexibility, and reduce daily discomfort from sitting or inactivity.
                    No matter your fitness background, this program is a perfect reset button for your body.`,
            rating: 4.5,
            reviews: 21
        },
        training_plan: [
            {
                title: "Monday routine",
                exercises: [
                    {
                        exercise: "Cat-Cow Stretch",
                        repeats: "10-12",
                        sets: "2",
                        duration: "-",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Shoulder Rolls + Arm Swings",
                        repeats: "20/2",
                        sets: "2",
                        duration: "-",
                        rest: "20 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Hip Circles",
                        repeats: "10/2",
                        sets: "2",
                        duration: "-",
                        rest: "20 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Deep Squat Hold + Spinal Twist",
                        repeats: "",
                        sets: "2",
                        duration: "30 sec",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Standing Hamstring Reach + Back Stretch",
                        repeats: "",
                        sets: "2",
                        duration: "30 sec",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Dynamic Lunge with Reach",
                        repeats: "10/2",
                        sets: "2",
                        duration: "",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Neck Mobility (Tilt, Turn, Nod)",
                        repeats: "10",
                        sets: "1",
                        duration: "",
                        rest: "",
                        description: "Description"
                    }
                ]
            },
            {
                title: "Monday routine",
                exercises: [
                    {
                        exercise: "Cat-Cow Stretch",
                        repeats: "10-12",
                        sets: "2",
                        duration: "-",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Shoulder Rolls + Arm Swings",
                        repeats: "20/2",
                        sets: "2",
                        duration: "-",
                        rest: "20 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Hip Circles",
                        repeats: "10/2",
                        sets: "2",
                        duration: "-",
                        rest: "20 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Deep Squat Hold + Spinal Twist",
                        repeats: "",
                        sets: "2",
                        duration: "30 sec",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Standing Hamstring Reach + Back Stretch",
                        repeats: "",
                        sets: "2",
                        duration: "30 sec",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Dynamic Lunge with Reach",
                        repeats: "10/2",
                        sets: "2",
                        duration: "",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Neck Mobility (Tilt, Turn, Nod)",
                        repeats: "10",
                        sets: "1",
                        duration: "",
                        rest: "",
                        description: "Description"
                    }
                ]
            },
            {
                title: "Monday routine",
                exercises: [
                    {
                        exercise: "Cat-Cow Stretch",
                        repeats: "10-12",
                        sets: "2",
                        duration: "-",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Shoulder Rolls + Arm Swings",
                        repeats: "20/2",
                        sets: "2",
                        duration: "-",
                        rest: "20 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Hip Circles",
                        repeats: "10/2",
                        sets: "2",
                        duration: "-",
                        rest: "20 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Deep Squat Hold + Spinal Twist",
                        repeats: "",
                        sets: "2",
                        duration: "30 sec",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Standing Hamstring Reach + Back Stretch",
                        repeats: "",
                        sets: "2",
                        duration: "30 sec",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Dynamic Lunge with Reach",
                        repeats: "10/2",
                        sets: "2",
                        duration: "",
                        rest: "30 sec",
                        description: "Description"
                    },
                    {
                        exercise: "Neck Mobility (Tilt, Turn, Nod)",
                        repeats: "10",
                        sets: "1",
                        duration: "",
                        rest: "",
                        description: "Description"
                    }
                ]
            },
        ],
        coach_data: {
            username: "trainerOne",
            profile_picture: kanye,
            rating: 4.8,
            reviews: 230,
        }
    }




    return (
        <Course {...training_data} />
    )
}

export default ExampleCoursePage