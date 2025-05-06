// For now, optional — add camera logic later if needed.
console.log("Fiawnt UI loaded.");

async function openCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      const video = document.getElementById('camera');
      video.srcObject = stream;
    } catch (err) {
      alert('Camera Error: ' + err.message);
    }
  }

function analyzeImage() {
    // Simulate analysis result
    const result = {
        seasonType: "Deep Autumn",
        seasonDesc: "Your rich and bold features give you a striking, intense look with natural depth.",
        undertone: "Warm",
        undertoneDesc: "Your skin has warm undertones, reflecting golden, peachy, or yellow hues in natural light.",
        recommendations: {
            foundations: [
                "Maybelline Fit Me Matte + Poreless",
                "L'Oréal True Match Super-Blendable",
                "Estée Lauder Double Wear"
            ],
            blushes: [
                "NARS Blush in Orgasm",
                "Milani Baked Blush in Luminoso",
                "MAC Powder Blush in Melba"
            ],
            lipsticks: [
                "MAC Chili",
                "Revlon Super Lustrous in Toast of New York",
                "Maybelline Creamy Matte in Touch of Spice"
            ]
        }
    };
    localStorage.setItem('analysisResult', JSON.stringify(result));
    window.location.href = 'details.html';
}