import './App.css';


const TransitDataItem = ({ item }) => {
    const getRectangleColor = (minutesUntilArrival) => {
      if (minutesUntilArrival <= 5) {
        return 'rgba(255, 0, 0, 0.5)';
      } else {
        return 'rgba(0, 255, 0, 0.5)';
      }
    };
  
    const getColorClass = (trainLine) => {
        if (['4', '5', '6'].includes(trainLine)) {
          return 'green-circle';
        } else {
          return 'yellow-circle';
        }
      };
    
      const parts = item.message.split(' ');
      const trainLine = parts[1];
      const colorClass = getColorClass(trainLine);
      const rectangleColor = getRectangleColor(item.minutes_until_arrival);
    
      return (
        <p>
          {parts[0]} <span className={`train-line-indicator ${colorClass}`}>{trainLine}</span> {parts.slice(2,5).join(' ')}
          <span
            style={{
              backgroundColor: rectangleColor,
              padding: '4px 4px',
              borderRadius: '4px',
              marginLeft: '10px'
            }}
          >
            {parts.slice(5,7).join(' ')} {/* Last two words, e.g., "in 2 minutes" */}
          </span>
        </p>
      );
    };
    
    export default TransitDataItem;

  