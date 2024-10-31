// hii ni indexPayPopUp.js ieke kwa base ndo iende kwa pages zote
document.addEventListener('DOMContentLoaded', () => {
  // Popup Logic
  const popUp = document.getElementById('pay-pop-up');
  const showPopups = document.querySelectorAll('.show-pop-up');
  const hidePopup = document.getElementById('pay-x');

  const competitionImage = popUp.querySelector('img');
  const carBrandElement = popUp.querySelector('#car_brand');
  const carModelElement = popUp.querySelector('#car_model');
  const formElement = popUp.querySelector('form');

  if (popUp && showPopups && hidePopup) {
    const show = (button) => {
      console.log('locating the neccessary')
      const competitionId = button.getAttribute('data-competition-id');
      const carBrand = button.getAttribute('data-car-brand');
      const carModel = button.getAttribute('data-car-model');
      const ticketPrice = button.getAttribute('data-ticket-price');
      const imageUrl = button.getAttribute('data-image-url'); // Assuming you have an image URL in the data attributes
      const formUrl = button.getAttribute('data-form-url');
      console.log(`${competitionId}, 
                   ${carBrand}, 
                   ${carModel}, 
                   ${ticketPrice}, 
                   ${imageUrl}`)
      console.log('values not found')

      // Update the popup fields with competition data
      carBrandElement.textContent = carBrand;
      carModelElement.textContent = carModel;
      ticketPriceElement.textContent = ticketPrice;
      totalPriceElement.textContent = ticketPrice; // Default to one ticket initially
      competitionImage.setAttribute('src', imageUrl); // Update image URL

      // Update form action URL
      formElement.setAttribute('action', `${formUrl}`);

      // Show the popup
      popUp.classList.remove('hidden');
      console.log(`Popup opened for competition ID: ${competitionId}`);
      console.log('values not found')
    };

    const hide = () => {
      popUp.classList.add('hidden');
    };

    showPopups.forEach(button => {
      button.addEventListener('click', () => {
        console.log('clicked')
        show(button); // Pass the button element to the show function
      });
    });

    hidePopup.addEventListener('click', hide);
  }

  // Quantity Increment/Decrement Logic
  const incrementButton = document.getElementById('increment');
  const decrementButton = document.getElementById('decrement');
  const quantityInput = document.getElementById('quantity');
  const ticketPriceElement = document.getElementById('ticket-price');
  const totalPriceElement = document.getElementById('total-price');

  if (incrementButton && decrementButton && quantityInput && ticketPriceElement && totalPriceElement) {
    const updateTotalPrice = () => {
      const quantity = parseInt(quantityInput.value);
      let ticketPrice = parseFloat(ticketPriceElement.textContent); // Ensure ticketPrice is a number

      if (isNaN(ticketPrice)) {
        console.error('Invalid ticket price:', ticketPriceElement.textContent);
        ticketPrice = 0; // Set default if ticket price is not valid
      }

      if (isNaN(quantity)) {
        console.error('Invalid quantity:', quantityInput.value);
        return; // Exit if quantity is invalid
      }

      const totalPrice = (ticketPrice * quantity).toFixed(2);
      totalPriceElement.textContent = totalPrice;
    };

    incrementButton.addEventListener('click', () => {
      let value = parseInt(quantityInput.value);
      if (value < 75) {
        quantityInput.value = value + 1;
        updateTotalPrice();
      }
    });

    decrementButton.addEventListener('click', () => {
      let value = parseInt(quantityInput.value);
      if (value > 1) {
        quantityInput.value = value - 1;
        updateTotalPrice();
      }
    });

    quantityInput.addEventListener('input', updateTotalPrice);
  }
});

// document.addEventListener('DOMContentLoaded', () => {
//     // Popup Logic
//     const popUp = document.getElementById('pop-up');
//     const showPopups = document.querySelectorAll('.show-pop-up');
//     const hidePopup = document.getElementById('x');

    
//     const competitionImage = popUp.querySelector('img');
//     const carBrandElement = popUp.querySelector('h2');
//     const carModelElement = popUp.querySelector('.my-1');
//     const formElement = popUp.querySelector('form');
  
//     if (popUp && showPopups && hidePopup) {
//       const show = (buttonId) => {

//         const competitionId = button.getAttribute('data-competition-id');
//         const carBrand = button.getAttribute('data-car-brand');
//         const carModel = button.getAttribute('data-car-model');
//         const ticketPrice = button.getAttribute('data-ticket-price');
  
//         // Update the popup fields with competition data
//         carBrandElement.textContent = carBrand;
//         carModelElement.textContent = carModel;
//         ticketPriceElement.textContent = ticketPrice;
//         totalPriceElement.textContent = ticketPrice; // Default to one ticket initially
  
//         // Update form action URL
//         formElement.setAttribute('action', /add_to_basket/${competitionId});

//         popUp.classList.remove('hidden');
//         console.log(Popup opened by button with ID: ${buttonId});
//       };
  
//       const hide = () => {
//         popUp.classList.add('hidden');
//       };
  
//       showPopups.forEach(button => {
//         button.addEventListener('click', () => {
//           show(button.id);
//         });
//       });
  
//       hidePopup.addEventListener('click', hide);
//     }

  
//     // Quantity Increment/Decrement Logic
//     const incrementButton = document.getElementById('increment');
//     const decrementButton = document.getElementById('decrement');
//     const quantityInput = document.getElementById('quantity');
//     const ticketPriceElement = document.getElementById('ticket-price');
//     const totalPriceElement = document.getElementById('total-price');
  
//     if (incrementButton && decrementButton && quantityInput && ticketPriceElement && totalPriceElement) {
//       console.log('we clear')
//       const ticketPrice = parseFloat(ticketPriceElement.textContent); // Base price per ticket
  
//       const updateTotalPrice = () => {
//         const quantity = parseInt(quantityInput.value);
//         const totalPrice = (ticketPrice * quantity).toFixed(2);
//         totalPriceElement.textContent = totalPrice;
//         updating
//       };
  
//       incrementButton.addEventListener('click', () => {
//         let value = parseInt(quantityInput.value);
//         if (value < 75) {
//           quantityInput.value = value + 1;
//           updateTotalPrice();
//         }
//       });
  
//       decrementButton.addEventListener('click', () => {
//         let value = parseInt(quantityInput.value);
//         if (value > 1) {
//           quantityInput.value = value - 1;
//           updateTotalPrice();
//         }
//       });
  
//       quantityInput.addEventListener('input', updateTotalPrice);
//     } else {
//       console.log('some fields not found')
//     }
  
//     // Quick Select Links Logic
//     const ticketInput = document.getElementById('quantity');
//     const quickSelectLinks = document.querySelectorAll('.quick-select');
  
//     if (quantityInput && quickSelectLinks) {
//       quickSelectLinks.forEach(link => {
//         link.addEventListener('click', (e) => {
//           e.preventDefault(); // Prevent default link behavior
//           const value = e.target.getAttribute('data-value');
//           quantityInput.value = value;
//           const event = new Event('input'); // Simulate input event for quantity update
//           quantityInput.dispatchEvent(event);
//         });
//       });
//     }
//   });