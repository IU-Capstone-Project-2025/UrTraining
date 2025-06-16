// import React from 'react'

const Step1Survey = () => {
    return (
        <>
            <div className="survey__title">
                <h2>
                    Let's know each other
                </h2>
            </div>
            <div className="survey__options__section">
                <p>
                    How can we call you?
                </p>
                <div className="survey__section__forms">
                    <form>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            className="form-basic-white"
                            placeholder="Name"
                        />
                        <input
                            type="text"
                            id="surname"
                            name="surname"
                            className="form-basic-white"
                            placeholder="Surname"
                        />
                    </form>
                </div>
            </div>
            <div className="survey__options__section">
                <p>
                    Where are you from?
                </p>
                <div className="survey__section__forms">
                    <form>
                        <select
                            name="country"
                            className="form-basic-white"
                        >
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                            <option>KAZAKHSTAN</option>
                        </select>
                        <input
                            type="text"
                            id="city"
                            name="city"
                            className="form-basic-white"
                            placeholder="City"
                        />
                    </form>
                </div>
            </div>
            <div className="survey__options__section">
                <p>
                    What is your gender?
                </p>
                <div className="survey__section__forms">
                    <form>
                        <label className="radio-basic-black">
                            <input
                                type="radio"
                                id="male"
                                name="gender"
                                value="male"
                            />
                            <div>Male</div>
                        </label>
                        <label className="radio-basic-black">
                            <input
                                type="radio"
                                id="female"
                                name="gender"
                                value="female"
                            />
                            <div>Female</div>
                        </label>
                    </form>
                </div>
            </div>
            <div className="survey__options__section">
                <p>
                    More data.
                </p>
                <div className="survey__section__forms">
                    <form>
                        <input
                            type="text"
                            id="age"
                            name="age"
                            className="form-basic-white"
                            placeholder="Age"
                        />
                        <input
                            type="text"
                            id="height"
                            name="height"
                            className="form-basic-white"
                            placeholder="Height"
                        />
                    </form>
                </div>
            </div>
        </>
    )
}

export default Step1Survey