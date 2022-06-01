import React, { useEffect, useState } from 'react'
import './comp-styles/Star-styles.css'

type Props = {
    num_stars: number
}

function StarRating(props: Props) {
    const [rating, setRating] = useState(0);

    const handleRating = () => {
        setRating(props.num_stars)
    }

    useEffect(handleRating, [props.num_stars]);

    return (
      <div className="star-rating">
        {[...Array(5)].map((star, index) => {
          index += 1;
          return (
            <span
              key={index}
              className={index <= rating ? "on" : "off"}
            >
              <span className="star">&#9733;</span>
            </span>
          );
        })}
      </div>
    )
}

export default StarRating