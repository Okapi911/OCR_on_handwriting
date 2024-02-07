export default function waitTime(nbPeople){
    if (nbPeople != NaN){
    let waitSeconds= nbPeople*75;
    let leftValue = Math.floor(waitSeconds/60);
    let rightValue= waitSeconds%60;
    return [leftValue, rightValue];}
}