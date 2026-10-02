const fs = require('fs');

function fixCottonQuotes(filePath) {
    let src = fs.readFileSync(filePath, 'utf8');
    
    // Fix quote collision
    src = src.replaceAll(
        "selectOnboardingCrop('cotton', '${getLocalizedCropName('cotton')}')",
        "selectOnboardingCrop('cotton', getLocalizedCropName('cotton'))"
    );
    src = src.replaceAll(
        "${getLocalizedCropName('cotton')}",
        "${getLocalizedCropName(\"cotton\")}"
    );

    fs.writeFileSync(filePath, src, 'utf8');
}

fixCottonQuotes('app/src/main/assets/index.html');
fixCottonQuotes('nukrop_emulator.html');
