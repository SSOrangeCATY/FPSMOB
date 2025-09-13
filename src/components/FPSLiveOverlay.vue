<template>
    <div class="fps-overlay">
      <div class="round-info">
        <div class="team-scores">
          <div class="team-info">
            <svg width="30" height="30" viewBox="0 0 30 30" class="team-logo" id="t_logo">
              <rect width="30" height="30" :fill="props.config.teamConfig?.tTeam?.color || '#FF9800'" rx="2"/>
              <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="10" id="t_name">{{ props.config.teamConfig?.tTeam?.name || 'T' }}</text>
            </svg>
            <span class="team-name" id="t_name" :style="{ marginLeft: teamNameMargin.t }">{{ props.config.teamConfig?.tTeam?.name || 'T' }}</span>
          </div>
          <div class="round-timer">
            <span class="team-score" id="t_score">{{ tWinnerRound }}</span>
            <div class="timer-content">
              <img v-if="bombPlanted" :src="bombIcon" alt="C4" class="c4-icon" />
              <span v-else class="round-number">{{ formatTime(roundTime) }}</span>
            </div>
            <span class="team-score" id="ct_score">{{ ctWinnerRound }}</span>
          </div>
          <div class="team-info">
            <svg width="30" height="30" viewBox="0 0 30 30" class="team-logo" id="ct_logo">
              <rect width="30" height="30" :fill="props.config.teamConfig?.ctTeam?.color || '#2196F3'" rx="2"/>
              <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="10" id="ct_name">{{ props.config.teamConfig?.ctTeam?.name || 'CT' }}</text>
            </svg>
            <span class="team-name" id="ct_name" :style="{ marginRight: teamNameMargin.ct }">{{ props.config.teamConfig?.ctTeam?.name || 'CT' }}</span>
          </div>
        </div>
  
        <div class="round-bottom-progress" :class="{ 'visible': bombPlanted || bombDefusing }" v-if="bombPlanted || bombDefusing">
          <div class="progress-track"></div>
          <div v-if="bombPlanted" class="progress-fill bomb" :style="{ width: bombPercent + '%' }"></div>
          <div v-if="bombDefusing && coverWidthPercent > 0" class="progress-fill cover" :style="{ width: coverWidthPercent + '%' }"></div>
          <div v-if="bombDefusing" class="progress-fill defuse" :style="{ left: defuseLeftPercent + '%', width: defuseWidthPercent + '%' }"></div>
        </div>
      </div>
  
    <!-- T方玩家信息 -->
    <div class="t_player-cards">
      <div 
        v-for="player in tSidePlayers" 
        :key="player.id"
        :class="['player-card', { 'alive': player.alive, 'dead': !player.alive }, 'left-card']"
      >
        <div class="player-header">
          <span class="player-name">{{ player.name }}</span>
          <div v-if="player.alive" class="kd-display">
            <div class="kd-values">
              <span class="kd-value">
                <svg t="1757288729344" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7062" ><path d="M502.656 448a56 56 0 1 0 0 112 56 56 0 0 0 0-112z m0-352C277.312 96 94.64 278.672 94.64 504S277.312 912 502.64 912C728 912 910.656 729.312 910.656 504S728 96 502.656 96zM544 829.312V688h-80v141.312C320 811.136 195.488 688 177.312 544H320v-80h-142.688C195.488 320 320 196.848 464 178.672V320h80v-141.328C688 196.848 809.808 320 827.968 464H688v80h139.968C809.824 688 688 811.152 544 829.312z" fill="#FFFFFF" p-id="7063"></path></svg>
                {{ player.kills }}
              </span>
              <span class="kd-value">
                <svg t="1757288453810" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6010" ><path d="M853.34016 384A298.65984 298.65984 0 0 0 554.65984 85.34016h-85.31968A298.65984 298.65984 0 0 0 170.65984 384v42.65984c0 24.6784 25.25184 29.65504 25.25184 42.68032 0 13.0048-25.25184 29.63456-25.25184 42.65984v42.65984A85.34016 85.34016 0 0 0 256 640h128v85.34016a42.65984 42.65984 0 0 0 42.65984 42.65984h21.34016v-42.65984h42.65984V768h42.68032v-42.65984h42.65984V768h21.34016a42.65984 42.65984 0 0 0 42.65984-42.65984V640h128a85.34016 85.34016 0 0 0 85.34016-85.34016V512c0-19.33312-25.25184-29.65504-25.25184-42.65984 0-13.02528 25.25184-20.6848 25.25184-42.68032V384z m-414.49472 88.76032c-20.7872 90.48064-54.00576 75.03872-97.81248 73.58464-46.4896-1.59744-77.57824-6.02112-87.32672-26.68544-23.8592-28.18048-20.15232-157.4912 94.67904-109.28128 51.99872 21.83168 96.91136 39.13728 90.46016 62.38208z m101.6832 181.3504c-22.36416 0-16.9984-25.94816-28.52864-25.76384-12.0832 0.24576-8.3968 25.76384-30.1056 25.76384a22.81472 22.81472 0 0 1-22.38464-28.83584 280.1664 280.1664 0 0 1 32.1536-63.36512 22.85568 22.85568 0 0 1 39.07584 0c13.37344 19.6608 24.20736 40.96 32.19456 63.36512a22.85568 22.85568 0 0 1-22.40512 28.83584z m228.49536-134.4512c-9.74848 20.6848-40.83712 25.088-87.32672 26.68544-43.78624 1.45408-77.0048 16.896-97.81248-73.58464-6.4512-23.2448 38.48192-40.5504 90.46016-62.38208 114.83136-48.2304 118.53824 81.1008 94.67904 109.28128z" fill="#FFFFFF" p-id="6011"></path><path d="M704 750.22336a85.34016 85.34016 0 0 1-85.34016 85.34016h-42.65984v39.1168h-42.65984v-39.1168h-42.68032v39.1168h-42.65984v-39.1168h-42.65984a85.34016 85.34016 0 0 1-85.34016-85.34016v-67.56352H256v116.30592a85.31968 85.31968 0 0 0 35.47136 69.2224l135.18848 97.3824 25.6-12.8a133.57056 133.57056 0 0 1 119.48032 0l25.6 12.8 135.18848-97.36192a85.34016 85.34016 0 0 0 35.47136-69.24288v-116.30592h-64v67.56352z" fill="#FFFFFF" p-id="6012"></path></svg>
                {{ player.deaths }}
              </span>
            </div>
          </div>
        </div>
      <span class="player-eco">{{ player.money }}</span>
        <div class="player-health">
        <div 
          v-if="player.status === 'alive'"
            class="health-bg" 
            :style="{ height: '33%', width: player.health + '%' }"
          />
          
          <template v-if="player.alive">
            <div class="health-with-shield">
              <span class="health-value">{{ player.health }}</span>
              <div class="shield-container" v-if="player.armor > 0">
                <svg t="1757288193319" alt="Shield" class="shield-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4635" width="200" height="200"><path d="M573.952 30.6176h0.0512l344.4224 104.448v439.0912c0 22.7328-0.512 35.84-2.6624 53.76a307.712 307.712 0 0 1-18.7904 75.1104c-24.6784 63.488-71.5264 123.4944-146.0224 179.0464-59.2896 44.1856-135.0144 84.6336-228.9152 120.9344l-10.3424 3.9936-10.2912-3.9936c-91.9552-35.5328-166.4512-75.0592-225.1776-118.2208-52.48-38.5024-91.6992-79.4624-119.3984-122.4704a317.1328 317.1328 0 0 1-45.3632-110.592c-5.2736-26.4192-6.4512-45.824-6.4512-77.568V134.9632l20.3776-6.144L456.1408 29.184c1.4848-0.4608 3.2256-1.0752 5.7856-2.1504A133.2224 133.2224 0 0 1 523.264 17.408c14.592 1.1776 27.648 4.4544 38.7584 8.9088 4.4544 1.792 8.3456 3.1744 12.032 4.3008z m287.232 146.8928L557.4144 85.4016a202.5472 202.5472 0 0 1-16.6912-5.888 75.776 75.776 0 0 0-22.016-5.0176 76.1344 76.1344 0 0 0-35.1232 5.5296c-4.096 1.6384-7.3728 2.8672-10.9568 3.9424L162.304 177.5104v396.6464c0 28.2112 1.024 44.544 5.376 66.3552 6.144 30.5664 17.92 60.6208 37.376 90.8288 23.7568 36.9664 58.1632 72.8576 105.1136 107.3152 52.224 38.4 118.9376 74.24 201.6256 106.9056 84.48-33.4336 152.2688-70.0928 205.0048-109.4144 66.048-49.2544 106.1888-100.6592 126.8736-153.856 7.9872-20.48 12.8-40.704 15.36-61.3376 1.792-15.0016 2.2016-26.2144 2.2016-46.7968V177.5104z" p-id="4636"></path></svg>
                <svg v-if="player.hasHelmet" alt="Helmet" class="helmet-icon" t="1757287937037" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3193" width="200" height="200"><path d="M771.136 642.88c27.072 51.232 23.424 109.12-10.944 173.728-34.336 64.576-117.088 105.536-248.192 122.944l259.136-296.64z m-68.16 5.824L461.664 928l-101.856-13.696 213.504-256.704 129.6-8.896zM512 64c222.688 0 403.2 179.296 403.2 459.136l44.8 22.048v44.064a1640.96 1640.96 0 0 1-55.68 11.424c5.056 26.24 7.616 63.264 7.616 110.944 0 49.6-26.688 113.152-80.064 190.624l-60.672-17.056c36.608-60 54.944-121.92 54.944-185.792 0-25.792-2.816-50.88-8.128-74.976l-2.272-9.472-28.608 3.712c-86.528 10.464-178.24 15.68-275.136 15.68-96.736 0-188.256-5.216-274.624-15.616l-28.64-3.68-2.24 9.376a348 348 0 0 0-8.096 74.976c0 63.84 18.304 125.76 54.944 185.792l-60.704 17.056c-53.344-77.472-80.032-141.024-80.032-190.624 0-47.648 2.528-84.608 7.584-110.976A1394.816 1394.816 0 0 1 64 589.248v-44.064c29.856-9.76 44.8-17.12 44.8-22.048C108.8 243.296 289.312 64 512 64zM232.832 642.88l259.712 18.56-190.432 215.488c-38.624-47.648-61.696-84.256-69.28-109.824-7.584-25.6-7.584-67.008 0-124.192zM620.448 211.52c-16.064-16.064-69.248-1.504-92.736 18.656l-1.024 0.896-2.112-1.088a16.896 16.896 0 0 0-2.208-0.768l-2.24-0.448a11.616 11.616 0 0 0-9.696 2.976l-119.776 119.776 0.64 0.576c-6.784-6.752-16.832-7.68-22.432-2.08l-18.752 18.72c-5.6 5.632-4.672 15.68 2.112 22.4l0.512 0.512-17.12 11.008c-6.016 6.048-5.056 16.8 2.208 24.064l67.488 67.488c7.232 7.232 18.016 8.224 24.032 2.176l11.008-17.152 0.48 0.544c6.784 6.784 16.8 7.712 22.4 2.112l18.752-18.752c5.632-5.6 4.672-15.648-2.08-22.4l0.672 0.704 119.776-119.776a11.616 11.616 0 0 0 2.976-9.696 15.68 15.68 0 0 0-2.432-6.656c20.64-22.88 35.872-77.44 19.552-93.76z m-249.92 200.16l49.792 49.792-6.784 10.592-53.6-53.568 10.592-6.816z m12.16-37.792l75.424 75.424-8.704 8.704-75.424-75.424 8.704-8.704z m220.448-145.024c0 5.44-0.992 13.824-4.256 24.448-3.84 12.544-9.664 24.224-15.68 31.712l-0.832 0.896L545.984 249.6c7.424-6.272 19.616-12.448 32.704-16.48 10.624-3.264 19.04-4.224 24.448-4.256z" p-id="3194"></path></svg>
              </div>
            </div>
            <div class="weapon-in-health">
              <span class="weapon-name">{{ player.weaponName }}</span>
            </div>
          </template>
          
          <template v-else>
            <div class="dead-stats-in-health">
              <div class="dead-adr">
                <span class="adr-label">ADR</span>
                <span class="adr-value">{{ player.adr || 0 }}</span>
              </div>
              <div class="dead-kd">
                <div class="kd-values">
                  <span class="kd-value">
                    <svg t="1757288729344" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7062" width="14" height="14"><path d="M502.656 448a56 56 0 1 0 0 112 56 56 0 0 0 0-112z m0-352C277.312 96 94.64 278.672 94.64 504S277.312 912 502.64 912C728 912 910.656 729.312 910.656 504S728 96 502.656 96zM544 829.312V688h-80v141.312C320 811.136 195.488 688 177.312 544H320v-80h-142.688C195.488 320 320 196.848 464 178.672V320h80v-141.328C688 196.848 809.808 320 827.968 464H688v80h139.968C809.824 688 688 811.152 544 829.312z" fill="#FFFFFF" p-id="7063"></path></svg>
                    {{ player.kills }}
                  </span>
                  <span class="kd-value">
                    <svg t="1757288453810" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6010" width="14" height="14"><path d="M853.34016 384A298.65984 298.65984 0 0 0 554.65984 85.34016h-85.31968A298.65984 298.65984 0 0 0 170.65984 384v42.65984c0 24.6784 25.25184 29.65504 25.25184 42.68032 0 13.0048-25.25184 29.63456-25.25184 42.65984v42.65984A85.34016 85.34016 0 0 0 256 640h128v85.34016a42.65984 42.65984 0 0 0 42.65984 42.65984h21.34016v-42.65984h42.65984V768h42.68032v-42.65984h42.65984V768h21.34016a42.65984 42.65984 0 0 0 42.65984-42.65984V640h128a85.34016 85.34016 0 0 0 85.34016-85.34016V512c0-19.33312-25.25184-29.65504-25.25184-42.65984 0-13.02528 25.25184-20.6848 25.25184-42.68032V384z m-414.49472 88.76032c-20.7872 90.48064-54.00576 75.03872-97.81248 73.58464-46.4896-1.59744-77.57824-6.02112-87.32672-26.68544-23.8592-28.18048-20.15232-157.4912 94.67904-109.28128 51.99872 21.83168 96.91136 39.13728 90.46016 62.38208z m101.6832 181.3504c-22.36416 0-16.9984-25.94816-28.52864-25.76384-12.0832 0.24576-8.3968 25.76384-30.1056 25.76384a22.81472 22.81472 0 0 1-22.38464-28.83584 280.1664 280.1664 0 0 1 32.1536-63.36512 22.85568 22.85568 0 0 1 39.07584 0c13.37344 19.6608 24.20736 40.96 32.19456 63.36512a22.85568 22.85568 0 0 1-22.40512 28.83584z m228.49536-134.4512c-9.74848 20.6848-40.83712 25.088-87.32672 26.68544-43.78624 1.45408-77.0048 16.896-97.81248-73.58464-6.4512-23.2448 38.48192-40.5504 90.46016-62.38208 114.83136-48.2304 118.53824 81.1008 94.67904 109.28128z" fill="#FFFFFF" p-id="6011"></path><path d="M704 750.22336a85.34016 85.34016 0 0 1-85.34016 85.34016h-42.65984v39.1168h-42.65984v-39.1168h-42.68032v39.1168h-42.65984v-39.1168h-42.65984a85.34016 85.34016 0 0 1-85.34016-85.34016v-67.56352H256v116.30592a85.31968 85.31968 0 0 0 35.47136 69.2224l135.18848 97.3824 25.6-12.8a133.57056 133.57056 0 0 1 119.48032 0l25.6 12.8 135.18848-97.36192a85.34016 85.34016 0 0 0 35.47136-69.24288v-116.30592h-64v67.56352z" fill="#FFFFFF" p-id="6012"></path></svg>
                    {{ player.deaths }}
                  </span>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- CT方玩家信息 -->
    <div class="ct_player-cards">
      <div 
        v-for="player in ctSidePlayers" 
        :key="player.id"
        :class="['player-card', { 'alive': player.alive, 'dead': !player.alive }, 'ct-card']"
        :id="player.id"
      >
        <div class="player-header">
          <span class="player-name">{{ player.name }}</span>
          <div v-if="player.alive" class="kd-display">
            <div class="kd-values">
                <span class="kd-value">
                  <svg t="1757288729344" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7062" width="14" height="14"><path d="M502.656 448a56 56 0 1 0 0 112 56 56 0 0 0 0-112z m0-352C277.312 96 94.64 278.672 94.64 504S277.312 912 502.64 912C728 912 910.656 729.312 910.656 504S728 96 502.656 96zM544 829.312V688h-80v141.312C320 811.136 195.488 688 177.312 544H320v-80h-142.688C195.488 320 320 196.848 464 178.672V320h80v-141.328C688 196.848 809.808 320 827.968 464H688v80h139.968C809.824 688 688 811.152 544 829.312z" fill="#FFFFFF" p-id="7063"></path></svg>
                  {{ player.kills }}
                </span>
                <span class="kd-value">
                  <svg t="1757288453810" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6010" width="14" height="14"><path d="M853.34016 384A298.65984 298.65984 0 0 0 554.65984 85.34016h-85.31968A298.65984 298.65984 0 0 0 170.65984 384v42.65984c0 24.6784 25.25184 29.65504 25.25184 42.68032 0 13.0048-25.25184 29.63456-25.25184 42.65984v42.65984A85.34016 85.34016 0 0 0 256 640h128v85.34016a42.65984 42.65984 0 0 0 42.65984 42.65984h21.34016v-42.65984h42.65984V768h42.68032v-42.65984h42.65984V768h21.34016a42.65984 42.65984 0 0 0 42.65984-42.65984V640h128a85.34016 85.34016 0 0 0 85.34016-85.34016V512c0-19.33312-25.25184-29.65504-25.25184-42.65984 0-13.02528 25.25184-20.6848 25.25184-42.68032V384z m-414.49472 88.76032c-20.7872 90.48064-54.00576 75.03872-97.81248 73.58464-46.4896-1.59744-77.57824-6.02112-87.32672-26.68544-23.8592-28.18048-20.15232-157.4912 94.67904-109.28128 51.99872 21.83168 96.91136 39.13728 90.46016 62.38208z m101.6832 181.3504c-22.36416 0-16.9984-25.94816-28.52864-25.76384-12.0832 0.24576-8.3968 25.76384-30.1056 25.76384a22.81472 22.81472 0 0 1-22.38464-28.83584 280.1664 280.1664 0 0 1 32.1536-63.36512 22.85568 22.85568 0 0 1 39.07584 0c13.37344 19.6608 24.20736 40.96 32.19456 63.36512a22.85568 22.85568 0 0 1-22.40512 28.83584z m228.49536-134.4512c-9.74848 20.6848-40.83712 25.088-87.32672 26.68544-43.78624 1.45408-77.0048 16.896-97.81248-73.58464-6.4512-23.2448 38.48192-40.5504 90.46016-62.38208 114.83136-48.2304 118.53824 81.1008 94.67904 109.28128z" fill="#FFFFFF" p-id="6011"></path><path d="M704 750.22336a85.34016 85.34016 0 0 1-85.34016 85.34016h-42.65984v39.1168h-42.65984v-39.1168h-42.68032v39.1168h-42.65984v-39.1168h-42.65984a85.34016 85.34016 0 0 1-85.34016-85.34016v-67.56352H256v116.30592a85.31968 85.31968 0 0 0 35.47136 69.2224l135.18848 97.3824 25.6-12.8a133.57056 133.57056 0 0 1 119.48032 0l25.6 12.8 135.18848-97.36192a85.34016 85.34016 0 0 0 35.47136-69.24288v-116.30592h-64v67.56352z" fill="#FFFFFF" p-id="6012"></path></svg>
                  {{ player.deaths }}
                </span>
              </div>
          </div>
        </div>
        <span class="player-eco">{{ player.money }}</span>
        <div class="player-health">
          <div 
          v-if="player.status === 'alive'"
            class="health-bg" 
            :style="{ height: '33%', width: player.health + '%' }"
          />
          
          <template v-if="player.status === 'alive'">
            <div class="weapon-in-health">
              <span class="weapon-name">{{ player.weaponName }}</span>
            </div>
            <div class="health-with-shield">
              <div class="shield-container" v-if="player.armor > 0">
                <svg v-if="player.hasHelmet" alt="Helmet" class="helmet-icon" t="1757287937037" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3193" width="200" height="200"><path d="M771.136 642.88c27.072 51.232 23.424 109.12-10.944 173.728-34.336 64.576-117.088 105.536-248.192 122.944l259.136-296.64z m-68.16 5.824L461.664 928l-101.856-13.696 213.504-256.704 129.6-8.896zM512 64c222.688 0 403.2 179.296 403.2 459.136l44.8 22.048v44.064a1640.96 1640.96 0 0 1-55.68 11.424c5.056 26.24 7.616 63.264 7.616 110.944 0 49.6-26.688 113.152-80.064 190.624l-60.672-17.056c36.608-60 54.944-121.92 54.944-185.792 0-25.792-2.816-50.88-8.128-74.976l-2.272-9.472-28.608 3.712c-86.528 10.464-178.24 15.68-275.136 15.68-96.736 0-188.256-5.216-274.624-15.616l-28.64-3.68-2.24 9.376a348 348 0 0 0-8.096 74.976c0 63.84 18.304 125.76 54.944 185.792l-60.704 17.056c-53.344-77.472-80.032-141.024-80.032-190.624 0-47.648 2.528-84.608 7.584-110.976A1394.816 1394.816 0 0 1 64 589.248v-44.064c29.856-9.76 44.8-17.12 44.8-22.048C108.8 243.296 289.312 64 512 64zM232.832 642.88l259.712 18.56-190.432 215.488c-38.624-47.648-61.696-84.256-69.28-109.824-7.584-25.6-7.584-67.008 0-124.192zM620.448 211.52c-16.064-16.064-69.248-1.504-92.736 18.656l-1.024 0.896-2.112-1.088a16.896 16.896 0 0 0-2.208-0.768l-2.24-0.448a11.616 11.616 0 0 0-9.696 2.976l-119.776 119.776 0.64 0.576c-6.784-6.752-16.832-7.68-22.432-2.08l-18.752 18.72c-5.6 5.632-4.672 15.68 2.112 22.4l0.512 0.512-17.12 11.008c-6.016 6.048-5.056 16.8 2.208 24.064l67.488 67.488c7.232 7.232 18.016 8.224 24.032 2.176l11.008-17.152 0.48 0.544c6.784 6.784 16.8 7.712 22.4 2.112l18.752-18.752c5.632-5.6 4.672-15.648-2.08-22.4l0.672 0.704 119.776-119.776a11.616 11.616 0 0 0 2.976-9.696 15.68 15.68 0 0 0-2.432-6.656c20.64-22.88 35.872-77.44 19.552-93.76z m-249.92 200.16l49.792 49.792-6.784 10.592-53.6-53.568 10.592-6.816z m12.16-37.792l75.424 75.424-8.704 8.704-75.424-75.424 8.704-8.704z m220.448-145.024c0 5.44-0.992 13.824-4.256 24.448-3.84 12.544-9.664 24.224-15.68 31.712l-0.832 0.896L545.984 249.6c7.424-6.272 19.616-12.448 32.704-16.48 10.624-3.264 19.04-4.224 24.448-4.256z" p-id="3194"></path></svg>
                <svg t="1757288193319" alt="Shield" class="shield-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4635" width="200" height="200"><path d="M573.952 30.6176h0.0512l344.4224 104.448v439.0912c0 22.7328-0.512 35.84-2.6624 53.76a307.712 307.712 0 0 1-18.7904 75.1104c-24.6784 63.488-71.5264 123.4944-146.0224 179.0464-59.2896 44.1856-135.0144 84.6336-228.9152 120.9344l-10.3424 3.9936-10.2912-3.9936c-91.9552-35.5328-166.4512-75.0592-225.1776-118.2208-52.48-38.5024-91.6992-79.4624-119.3984-122.4704a317.1328 317.1328 0 0 1-45.3632-110.592c-5.2736-26.4192-6.4512-45.824-6.4512-77.568V134.9632l20.3776-6.144L456.1408 29.184c1.4848-0.4608 3.2256-1.0752 5.7856-2.1504A133.2224 133.2224 0 0 1 523.264 17.408c14.592 1.1776 27.648 4.4544 38.7584 8.9088 4.4544 1.792 8.3456 3.1744 12.032 4.3008z m287.232 146.8928L557.4144 85.4016a202.5472 202.5472 0 0 1-16.6912-5.888 75.776 75.776 0 0 0-22.016-5.0176 76.1344 76.1344 0 0 0-35.1232 5.5296c-4.096 1.6384-7.3728 2.8672-10.9568 3.9424L162.304 177.5104v396.6464c0 28.2112 1.024 44.544 5.376 66.3552 6.144 30.5664 17.92 60.6208 37.376 90.8288 23.7568 36.9664 58.1632 72.8576 105.1136 107.3152 52.224 38.4 118.9376 74.24 201.6256 106.9056 84.48-33.4336 152.2688-70.0928 205.0048-109.4144 66.048-49.2544 106.1888-100.6592 126.8736-153.856 7.9872-20.48 12.8-40.704 15.36-61.3376 1.792-15.0016 2.2016-26.2144 2.2016-46.7968V177.5104z" p-id="4636"></path></svg>
              </div>
              <span class="health-value">{{ player.health }}</span>
            </div>
          </template>
          
          <template v-else>
            <div class="dead-stats-in-health">
              <div class="dead-adr">
                <span class="adr-label">ADR</span>
                <span class="adr-value">{{ player.adr || 0 }}</span>
              </div>
              <div class="dead-kd">
                <div class="kd-values">
                    <span class="kd-value">
                      <svg t="1757288729344" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7062" width="14" height="14"><path d="M502.656 448a56 56 0 1 0 0 112 56 56 0 0 0 0-112z m0-352C277.312 96 94.64 278.672 94.64 504S277.312 912 502.64 912C728 912 910.656 729.312 910.656 504S728 96 502.656 96zM544 829.312V688h-80v141.312C320 811.136 195.488 688 177.312 544H320v-80h-142.688C195.488 320 320 196.848 464 178.672V320h80v-141.328C688 196.848 809.808 320 827.968 464H688v80h139.968C809.824 688 688 811.152 544 829.312z" fill="#FFFFFF" p-id="7063"></path></svg>
                      {{ player.kills }}
                    </span>
                    <span class="kd-value">
                      <svg t="1757288453810" class="kd-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="6010" width="14" height="14"><path d="M853.34016 384A298.65984 298.65984 0 0 0 554.65984 85.34016h-85.31968A298.65984 298.65984 0 0 0 170.65984 384v42.65984c0 24.6784 25.25184 29.65504 25.25184 42.68032 0 13.0048-25.25184 29.63456-25.25184 42.65984v42.65984A85.34016 85.34016 0 0 0 256 640h128v85.34016a42.65984 42.65984 0 0 0 42.65984 42.65984h21.34016v-42.65984h42.65984V768h42.68032v-42.65984h42.65984V768h21.34016a42.65984 42.65984 0 0 0 42.65984-42.65984V640h128a85.34016 85.34016 0 0 0 85.34016-85.34016V512c0-19.33312-25.25184-29.65504-25.25184-42.65984 0-13.02528 25.25184-20.6848 25.25184-42.68032V384z m-414.49472 88.76032c-20.7872 90.48064-54.00576 75.03872-97.81248 73.58464-46.4896-1.59744-77.57824-6.02112-87.32672-26.68544-23.8592-28.18048-20.15232-157.4912 94.67904-109.28128 51.99872 21.83168 96.91136 39.13728 90.46016 62.38208z m101.6832 181.3504c-22.36416 0-16.9984-25.94816-28.52864-25.76384-12.0832 0.24576-8.3968 25.76384-30.1056 25.76384a22.81472 22.81472 0 0 1-22.38464-28.83584 280.1664 280.1664 0 0 1 32.1536-63.36512 22.85568 22.85568 0 0 1 39.07584 0c13.37344 19.6608 24.20736 40.96 32.19456 63.36512a22.85568 22.85568 0 0 1-22.40512 28.83584z m228.49536-134.4512c-9.74848 20.6848-40.83712 25.088-87.32672 26.68544-43.78624 1.45408-77.0048 16.896-97.81248-73.58464-6.4512-23.2448 38.48192-40.5504 90.46016-62.38208 114.83136-48.2304 118.53824 81.1008 94.67904 109.28128z" fill="#FFFFFF" p-id="6011"></path><path d="M704 750.22336a85.34016 85.34016 0 0 1-85.34016 85.34016h-42.65984v39.1168h-42.65984v-39.1168h-42.68032v39.1168h-42.65984v-39.1168h-42.65984a85.34016 85.34016 0 0 1-85.34016-85.34016v-67.56352H256v116.30592a85.31968 85.31968 0 0 0 35.47136 69.2224l135.18848 97.3824 25.6-12.8a133.57056 133.57056 0 0 1 119.48032 0l25.6 12.8 135.18848-97.36192a85.34016 85.34016 0 0 0 35.47136-69.24288v-116.30592h-64v67.56352z" fill="#FFFFFF" p-id="6012"></path></svg>
                      {{ player.deaths }}
                    </span>
                  </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 广告栏 -->
    <div 
      v-if="shouldShowAd"
      class="ad-banner"
      :class="adPositionClass"
    >
      <img 
        v-if="adConfig.imageUrl" 
        :src="adConfig.imageUrl" 
        alt="ad" 
        class="ad-image"
      />
      <span v-if="adConfig.text" class="ad-text">{{ adConfig.text }}</span>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, defineProps, watch, computed } from 'vue'
  
  const props = defineProps({
    config: {
      type: Object,
      required: true,
      default: () => ({
        uiConfig: {},
        styleConfig: {},
        teamConfig: {
          ctTeam: { name: 'CT', icon: 'ct_logo.svg', color: '#2196F3' },
          tTeam: { name: 'T', icon: 't_logo.svg', color: '#FF9800' },
        },
        syncConfig: {
          syncMode: 'active',
          syncInterval: 5000,
          apiUrl: '',
          apiKey: '',
          localFilePath: '',
          localFileInterval: 10,
        },
      }),
    },
  })
  
  const tSidePlayers = ref([])
  const ctSidePlayers = ref([])
  const ctWinnerRound = ref(0)
  const tWinnerRound = ref(0)
  const currentRound = ref(0)
  const roundTime = ref(0)
  const FuseTime = ref(0)
  const bombPlanted = ref(false)
  const bombDefusing = ref(false)
  const roundStatus = ref('live')
  const bombFuse = ref(0)
  const bombTotalFuse = ref(800)
  const dismantleBombProgress = ref(0)
  const isAdVisible = ref(false)
  let adCycleInterval = null
  let adHideTimeout = null
  
  const bombPercent = computed(() => {
    const fuse = Number(bombFuse.value || 0)
    const total = Number(bombTotalFuse.value || 100)
    return Math.max(0, Math.min(100, ((total - fuse) / total) * 100))
  })
  const defusePercent = computed(() => {
    return Math.max(0, Math.min(100, (Number(dismantleBombProgress.value || 0) * 100)))
  })
  
  const defuseLeftPercent = computed(() => {
    const defuse = defusePercent.value
    return Math.max(0, Math.min(100, Math.min(defuse, bombPercent.value)))
  })
  
  const defuseWidthPercent = computed(() => {
    const defuse = defusePercent.value
    return Math.max(0, defuse - defuseLeftPercent.value)
  })
  const coverWidthPercent = computed(() => {
    return Math.max(0, Math.min(bombPercent.value, defusePercent.value))
  })
  
  // C4 图片
  const bombIcon = new URL('/src/assets/c4_3.png', import.meta.url).href
  
  const teamNameLength = ref({ t: 0, ct: 0 })
  const teamNameMargin = ref({ t: '0px', ct: '0px' })
  
  function calculateTeamNameSymmetry() {
    const tName = props.config.teamConfig?.tTeam?.name || 'T'
    const ctName = props.config.teamConfig?.ctTeam?.name || 'CT'
    const tLength = tName.length
    const ctLength = ctName.length
    const diff = Math.abs(tLength - ctLength)
    if (tLength > ctLength) {
      teamNameMargin.value = { t: '0px', ct: `${diff * 4}px` }
    } else if (ctLength > tLength) {
      teamNameMargin.value = { t: `${diff * 4}px`, ct: '0px' }
    } else {
      teamNameMargin.value = { t: '0px', ct: '0px' }
    }
    teamNameLength.value = { t: tLength, ct: ctLength }
  }
  
  watch(() => props.config.teamConfig, () => {
    calculateTeamNameSymmetry()
  }, { deep: true, immediate: true })
  
  function formatTime(totalSeconds) {
    const seconds = Math.max(0, Math.floor(totalSeconds || 0))
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    const minutesPart = mins.toString().padStart(2, '0')
    const secondsPart = secs.toString().padStart(2, '0')
    return `${minutesPart}:${secondsPart}`
  }
  
  async function fetchGameData() {
    try {
      const response = await fetch('/api/data')
      if (response.ok) {
        return await response.json()
      }
      return null
    } catch (e) {
      console.error(e)
      return null
    }
  }
  
  async function initializePlayersFromApi() {
    const apiMessage = await fetchGameData()
    if (apiMessage && apiMessage.tabData) {
      ctWinnerRound.value = apiMessage.cTWinnerRounds || 0
      tWinnerRound.value = apiMessage.tWinnerRounds || 0
      currentRound.value = (apiMessage.tWinnerRounds || 0) + (apiMessage.cTWinnerRounds || 0) + 1
      const timeTicksOrSeconds = apiMessage.time || 0
      roundTime.value = timeTicksOrSeconds / 20
  
      bombFuse.value = apiMessage.bombFuse || 0
      bombTotalFuse.value = apiMessage.bombTotalFuse || 100
      dismantleBombProgress.value = apiMessage.dismantleBombProgress || 0
      bombPlanted.value = bombFuse.value > 0
      bombDefusing.value = dismantleBombProgress.value > 0
  
      if (apiMessage.isWarmTime) {
        roundStatus.value = 'warmup'
      } else if (apiMessage.isPause) {
        roundStatus.value = 'pause'
      } else if (bombPlanted.value) {
        roundStatus.value = 'bomb_planted'
      } else if (bombDefusing.value) {
        roundStatus.value = 'bomb_defusing'
      } else {
        roundStatus.value = 'live'
      }
  
      const currentPlayerIds = new Set()
      Object.keys(apiMessage.tabData).forEach(playerId => {
        currentPlayerIds.add(playerId)
        const rawPlayerData = apiMessage.tabData[playerId]
        const team = rawPlayerData.team
        
        // 检查玩家是否已存在，如果存在且队伍不同，先移除
        const existingTIndex = tSidePlayers.value.findIndex(p => p.id === playerId)
        const existingCTIndex = ctSidePlayers.value.findIndex(p => p.id === playerId)
        if (existingTIndex !== -1 && team !== 't') {
          tSidePlayers.value.splice(existingTIndex, 1)
        }
        if (existingCTIndex !== -1 && team !== 'ct') {
          ctSidePlayers.value.splice(existingCTIndex, 1)
        }
        
        const playerData = {
          id: playerId,
          rawData: rawPlayerData,
          get name() { return this.rawData.name || this.rawData.data?.name || 'Unknown' },
          get kills() { return (this.rawData.kills ?? this.rawData.data?.kills ?? 0) },
          get deaths() { return (this.rawData.deaths ?? this.rawData.data?.deaths ?? 0) },
          get health() { return Math.round(this.rawData.health || 0) },
          get money() { const m = (this.rawData.money ?? this.rawData.data?.money ?? 0); return `$${m}` },
          get hasHelmet() { return this.rawData.bpAttributeHasHelmet || false },
          get armor() {
            const d = this.rawData.bpAttributeDurability
            if (d == null) return 0
            return d <= 1 ? Math.round(d * 100) : d
          },
          get alive() { return this.rawData.living || false },
          get status() { return this.alive ? 'alive' : 'dead' },
          get damage() { return (this.rawData.damage ?? this.rawData.data?.damage ?? 0) },
          get adr() { return currentRound.value > 0 ? Math.round(this.damage / currentRound.value) : 0 },
          get weaponName() {
            const items = this.rawData.items || {}
            const main = Array.isArray(items.MAIN_WEAPON) ? items.MAIN_WEAPON : []
            if (main.length > 0) return main[0]
            const secondary = Array.isArray(items.SECONDARY_WEAPON) ? items.SECONDARY_WEAPON : []
            if (secondary.length > 0) return secondary[0]
            const third = Array.isArray(items.THIRD_WEAPON) ? items.THIRD_WEAPON : []
            if (third.length > 0) return third[0]
            const carried = Array.isArray(items.CARRIED) ? items.CARRIED : []
            if (carried.length > 0) return carried[0]
            return ''
          },
          get team() { return team },
          get element() { return document.getElementById(this.id) },
        }

        // 添加到对应队伍
        if (team === 't') {
          const existingIndex = tSidePlayers.value.findIndex(p => p.id === playerId)
          if (existingIndex !== -1) {
            tSidePlayers.value[existingIndex].rawData = rawPlayerData
          } else {
            tSidePlayers.value.push(playerData)
          }
        } else if (team === 'ct') {
          const existingIndex = ctSidePlayers.value.findIndex(p => p.id === playerId)
          if (existingIndex !== -1) {
            ctSidePlayers.value[existingIndex].rawData = rawPlayerData
          } else {
            ctSidePlayers.value.push(playerData)
          }
        }
      })
  
      tSidePlayers.value = tSidePlayers.value.filter(player => currentPlayerIds.has(player.id))
      ctSidePlayers.value = ctSidePlayers.value.filter(player => currentPlayerIds.has(player.id))
    }
  }
  
  let updateInterval = null
  
  watch(() => props.config, (newConfig) => {
    applyConfigStyles(newConfig.styleConfig)
    updateTeamInfo(newConfig.teamConfig)
    if (newConfig && newConfig.teamConfig) {
      updateTeamInfo()
      loadTeamIcons()
    }
  }, { deep: true })
  
  function loadTeamIcons() {
    if (!props.config?.teamConfig) return
    const { ctTeam, tTeam } = props.config.teamConfig
    const ctIconPath = ctTeam?.icon ? new URL(`/src/assets/${ctTeam.icon}`, import.meta.url).href : null
    loadTeamIcon('ct', ctIconPath, ctTeam?.color || '#2196F3', ctTeam?.name || 'CT')
    const tIconPath = tTeam?.icon ? new URL(`/src/assets/${tTeam.icon}`, import.meta.url).href : null
    loadTeamIcon('t', tIconPath, tTeam?.color || '#FF5722', tTeam?.name || 'T')
  }
  
  function updateTeamInfo(teamConfig) {
    if (teamConfig) {
      iconLoadStatus.value.t.loaded = false
      iconLoadStatus.value.t.error = false
      iconLoadStatus.value.ct.loaded = false
      iconLoadStatus.value.ct.error = false
      const tLogo = document.getElementById('t_logo')
      const tName = document.getElementById('t_name')
      if (tLogo && teamConfig.tTeam) {
        loadTeamIcon('t', teamConfig.tTeam.icon, teamConfig.tTeam.color, teamConfig.tTeam.name || 'T')
      }
      if (tName && teamConfig.tTeam) {
        tName.textContent = teamConfig.tTeam.name || 'T'
      }
      const ctLogo = document.getElementById('ct_logo')
      const ctName = document.getElementById('ct_name')
      if (ctLogo && teamConfig.ctTeam) {
        loadTeamIcon('ct', teamConfig.ctTeam.icon, teamConfig.ctTeam.color, teamConfig.ctTeam.name || 'CT')
      }
      if (ctName && teamConfig.ctTeam) {
        ctName.textContent = teamConfig.ctTeam.name || 'CT'
      }
    }
  }
  
  const iconLoadStatus = ref({
    t: { loaded: false, error: false },
    ct: { loaded: false, error: false },
  })
  
  function loadTeamIcon(teamType, iconPath, fallbackColor, fallbackText) {
    const logoElement = document.getElementById(`${teamType}_logo`)
    if (!logoElement) return
    if (!iconPath) {
      showSvgPlaceholder(logoElement, fallbackColor, fallbackText)
      return
    }
    if (logoElement.tagName === 'IMG') {
      logoElement.src = iconPath
      return
    }
    const img = new Image()
    img.onload = () => {
      iconLoadStatus.value[teamType].loaded = true
      iconLoadStatus.value[teamType].error = false
      if (logoElement.tagName === 'svg') {
        const parent = logoElement.parentElement
        const newImg = document.createElement('img')
        newImg.src = iconPath
        newImg.alt = `${fallbackText} Logo`
        newImg.className = 'team-logo'
        newImg.style.width = '30px'
        newImg.style.height = '30px'
        newImg.style.objectFit = 'contain'
        parent.replaceChild(newImg, logoElement)
      } else {
        logoElement.src = iconPath
      }
    }
    img.onerror = () => {
      iconLoadStatus.value[teamType].loaded = false
      iconLoadStatus.value[teamType].error = true
      showSvgPlaceholder(logoElement, fallbackColor, fallbackText)
    }
    img.src = iconPath
  }
  
  function showSvgPlaceholder(logoElement, color, text) {
    if (logoElement.tagName === 'IMG') {
      const parent = logoElement.parentElement
      const newSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
      newSvg.setAttribute('width', '30')
      newSvg.setAttribute('height', '30')
      newSvg.setAttribute('viewBox', '0 0 30 30')
      newSvg.className = 'team-logo'
      newSvg.id = logoElement.id
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
      rect.setAttribute('width', '30')
      rect.setAttribute('height', '30')
      rect.setAttribute('fill', color)
      rect.setAttribute('rx', '2')
      const textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text')
      textElement.setAttribute('x', '50%')
      textElement.setAttribute('y', '50%')
      textElement.setAttribute('dominant-baseline', 'middle')
      textElement.setAttribute('text-anchor', 'middle')
      textElement.setAttribute('fill', 'white')
      textElement.setAttribute('font-size', '10')
      textElement.textContent = text
      newSvg.appendChild(rect)
      newSvg.appendChild(textElement)
      parent.replaceChild(newSvg, logoElement)
    } else {
      const rect = logoElement.querySelector('rect')
      const textElement = logoElement.querySelector('text')
      if (rect) rect.setAttribute('fill', color)
      if (textElement) textElement.textContent = text
    }
    logoElement.style.display = 'block'
  }
  
  function applyConfigStyles(styleConfig) {
    if (styleConfig.fontFamily) {
      document.documentElement.style.setProperty('--font-family', styleConfig.fontFamily)
    }
    if (styleConfig.customCSS) {
      const styleElement = document.getElementById('custom-css') || document.createElement('style')
      styleElement.id = 'custom-css'
      styleElement.textContent = styleConfig.customCSS
      document.head.appendChild(styleElement)
    }
  }
  
  onMounted(() => {
    applyConfigStyles(props.config.styleConfig || {})
    loadTeamIcons()
    updateInterval = setInterval(() => {
      initializePlayersFromApi()
    }, 50)
    setupAdCycle()
  })
  
  onUnmounted(() => {
    if (updateInterval) {
      clearInterval(updateInterval)
    }
    const customStyle = document.getElementById('custom-css')
    if (customStyle) customStyle.remove()
    if (adCycleInterval) {
      clearInterval(adCycleInterval)
      adCycleInterval = null
    }
    if (adHideTimeout) {
      clearTimeout(adHideTimeout)
      adHideTimeout = null
    }
  })

  // ===== 广告配置与显示逻辑 =====
  const uiConfig = computed(() => props.config?.uiConfig || {})
  const adConfig = computed(() => {
    const cfg = uiConfig.value?.adCardConfig || {}
    return {
      enabled: cfg.enabled ?? false,
      text: cfg.text || '',
      imageUrl: cfg.imageUrl || '',
      position: cfg.position || 'bottom-right',
      duration: Number(cfg.duration || 30),
      interval: Number(cfg.interval || 300),
    }
  })
  const shouldShowAd = computed(() => (uiConfig.value.showAdCard && adConfig.value.enabled && isAdVisible.value))
  const adPositionClass = computed(() => {
    const pos = adConfig.value.position
    return {
      'pos-top-left': pos === 'top-left',
      'pos-top-right': pos === 'top-right',
      'pos-bottom-left': pos === 'bottom-left',
      'pos-bottom-right': pos === 'bottom-right',
    }
  })
  function clearAdTimers() {
    if (adCycleInterval) {
      clearInterval(adCycleInterval)
      adCycleInterval = null
    }
    if (adHideTimeout) {
      clearTimeout(adHideTimeout)
      adHideTimeout = null
    }
  }
  function setupAdCycle() {
    clearAdTimers()
    // 若广告未启用，或未选中显示，则不启动
    if (!(uiConfig.value.showAdCard && adConfig.value.enabled)) {
      isAdVisible.value = false
      return
    }
    // 立即显示一次
    isAdVisible.value = true
    adHideTimeout = setTimeout(() => {
      isAdVisible.value = false
    }, Math.max(1, adConfig.value.duration) * 1000)
    // 周期性显示
    adCycleInterval = setInterval(() => {
      isAdVisible.value = true
      if (adHideTimeout) clearTimeout(adHideTimeout)
      adHideTimeout = setTimeout(() => {
        isAdVisible.value = false
      }, Math.max(1, adConfig.value.duration) * 1000)
    }, Math.max(adConfig.value.duration + 1, adConfig.value.interval) * 1000)
  }
  watch(() => props.config?.uiConfig, () => {
    setupAdCycle()
  }, { deep: true })
  </script>
  
  <style scoped>
  .fps-overlay {
    position: relative;
  }
  .round-info {
    position: relative;
  }
  .team-scores {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .round-timer {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .timer-content {
    min-width: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .round-number {
    font-size: 18px;
    font-weight: 700;
  }
  .c4-icon {
    width: 32px;
    height: 32px;
    object-fit: contain;
  }
  /* ===== 广告样式 ===== */
  .ad-banner {
    position: absolute;
    z-index: 10;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: rgba(0,0,0,0.6);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 6px;
    backdrop-filter: blur(6px);
    color: #fff;
  }
  .ad-banner.pos-top-left { top: 12px; left: 12px; }
  .ad-banner.pos-top-right { top: 12px; right: 12px; }
  .ad-banner.pos-bottom-left { bottom: 12px; left: 12px; }
  .ad-banner.pos-bottom-right { bottom: 12px; right: 12px; }
  .ad-image { height: 32px; width: auto; object-fit: contain; }
  .ad-text { font-size: 14px; font-weight: 600; }
  .round-bottom-progress {
    position: absolute;
    left: 6px;
    right: 6px;
    bottom: 0;
    height: 8px;
    z-index: 2;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  .round-bottom-progress.visible {
    opacity: 1;
    transform: translateY(0);
  }
  .progress-track {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    background: #4C4C4A;
    border-radius: 0;
    z-index: 0;
  }
  .progress-fill {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    border-radius: 0;
    transition: width 0.3s ease, left 0.3s ease;
  }
  .progress-fill.bomb {
    background: linear-gradient(90deg, #ff9800, #ff4500);
    z-index: 1;
  }
  .progress-fill.cover {
    background: #4C4C4A;
    z-index: 2;
  }
  .progress-fill.defuse {
    background: #4fc3f7;
    height: 8px;
    top: 0;
    z-index: 3;
  }
  /* ===== 玩家卡片（死亡态修复）==== */
  .player-card.dead .weapon-in-health { display: none; }
  .player-card.dead .health-with-shield { display: none; }
  .player-card.dead .dead-stats-in-health {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    gap: 12px;
    text-align: center;
  }
  .player-card.dead .dead-adr, .player-card.dead .dead-kd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  .t_player-cards .left-card.player-card.dead {
    opacity: 0.85;
  }
  </style>