<template>
  <div class="fps-overlay">
    <!-- 回合信息 -->
    <div class="round-info">
      <div class="team-scores">
        <div class="team-info">
          <svg width="30" height="30" viewBox="0 0 30 30" class="team-logo" id="t_logo">
            <rect width="30" height="30" fill="#FF9800" rx="2"/>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="10" id="t_name">Spirit</text>
          </svg>
          <span class="team-name" id="t_name">Spirit</span>
          <span class="team-score" id="t_score">{{ tWinnerRound }}</span>
        </div>
        <div class="round-timer">
          <span class="round-number">1:03</span>
        </div>
        <div class="team-info">
          <span class="team-score" id="ct_score">{{ ctWinnerRound }}</span>
          <span class="team-name" id="ct_name">FaZe</span>
          <svg width="30" height="30" viewBox="0 0 30 30" class="team-logo" id="ct_logo">
            <rect width="30" height="30" fill="#2196F3" rx="2"/>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="10" id="ct_name">FaZe</text>
          </svg>
        </div>
      </div>
    </div>

    <!-- 左下角玩家信息 -->
    <div class="t_player-cards">
      <!-- T方玩家 -->
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
        <div v-if="player.status === 'alive'" class="player-health">
          <div 
            class="health-bg"
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

    <!-- 赞助商广告 -->
    <div class="sponsor-banner">
      <svg width="120" height="30" viewBox="0 0 120 30">
        <rect width="120" height="30" fill="#1A1A1A" rx="4"/>
        <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="10">MCCS2</text>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps, watch } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    required: true,
    default: () => ({
      apiConfig: {},
      uiConfig: {},
      styleConfig: {}
    })
  }
})

const tSidePlayers = ref([])
const ctSidePlayers = ref([])
const ctWinnerRound = ref(0)
const tWinnerRound = ref(0)
const currentRound = ref(0)
const roundTime = ref(0)
const FuseTime = ref(0)

// 从API获取数据
async function fetchGameData() {
  try {
    const response = await fetch('/api/data')
    if (response.ok) {
      return await response.json()
    } else {
      console.error('Failed to fetch game data:', response.status)
      return null
    }
  } catch (error) {
    console.error('Error fetching game data:', error)
    return null
  }
}

// 从API数据初始化玩家数据 - 直接使用API数据作为引用
async function initializePlayersFromApi() {
  // 从API获取数据
  const apiMessage = await fetchGameData()  
  if (apiMessage && apiMessage.tabData) {
    // 计算当前总回合数
    ctWinnerRound.value = apiMessage.cTWinnerRounds || 0
    tWinnerRound.value = apiMessage.tWinnerRounds || 0
    currentRound.value = (apiMessage.tWinnerRounds || 0) + (apiMessage.cTWinnerRounds || 0) + 1
    
    // 记录当前API中的所有玩家ID，用于后续清理不存在的玩家
    const currentPlayerIds = new Set()
    
    // 遍历API数据中的tabData获取玩家数据
    Object.keys(apiMessage.tabData).forEach(playerId => {
      currentPlayerIds.add(playerId)
      
      // 获取原始API数据
      const rawPlayerData = apiMessage.tabData[playerId]
      
      // 计算需要的派生数据
      const team = rawPlayerData.team

      // 创建玩家数据引用，保留原始数据结构的引用
      const playerData = {
        // 直接引用原始数据的关键属性
        id: playerId,
        rawData: rawPlayerData,        
        // 计算属性，但使用getter确保每次访问都是最新值
        get name() { return this.rawData.name || this.rawData.data?.name || 'Unknown' },
        get kills() { return this.rawData.data?.kills || 0 },
        get deaths() { return this.rawData.data?.deaths || 0 },
        get health() { return this.rawData.health || 0 },
        get money() { return "$"+ this.rawData.money || 0 },
        get hasHelmet() { return this.rawData.bpAttributeHasHelmet || false },
        get armor() { return this.rawData.bpAttributeDurability || 0 },
        get alive() { return this.rawData.living || false },
        get status() { return this.alive ? 'alive' : 'dead' },
        get damage() { return this.rawData.data?.damage || 0},
        get adr() { return currentRound.value > 0 ? Math.round(this.damage / currentRound.value) : 0 },
        get weaponName() { return this.rawData.items && this.rawData.items.CARRIED && this.rawData.items.CARRIED.length > 0 ? this.rawData.items.CARRIED[0] : '' },
        get team() { return team },
        get element() {
          return document.getElementById(this.id)
        }
      }
      
      // 尝试查找现有玩家
      const existingPlayerIndex = team === 't' 
        ? tSidePlayers.value.findIndex(p => p.id === playerId)
        : ctSidePlayers.value.findIndex(p => p.id === playerId)
      
      // 如果玩家已存在，更新其rawData引用
      if (existingPlayerIndex !== -1) {
        if (team === 't') {
          tSidePlayers.value[existingPlayerIndex].rawData = rawPlayerData
        } else {
          ctSidePlayers.value[existingPlayerIndex].rawData = rawPlayerData
        }
      } else {
        // 如果玩家不存在，添加新玩家数据引用
        if (team === 't') {
          tSidePlayers.value.push(playerData)
        } else if (team === 'ct') {
          ctSidePlayers.value.push(playerData)
        }
      }
    })
    
    // 清理不存在的玩家
    tSidePlayers.value = tSidePlayers.value.filter(player => currentPlayerIds.has(player.id))
    ctSidePlayers.value = ctSidePlayers.value.filter(player => currentPlayerIds.has(player.id))
  }
}

// 定时器引用
let updateInterval = null

// 监听配置变化
watch(() => props.config, (newConfig) => {
  // 当配置变化时，可以重新应用样式或调整显示逻辑
  applyConfigStyles(newConfig.styleConfig)
}, { deep: true })

// 应用配置样式
function applyConfigStyles(styleConfig) {
  // 应用字体设置
  if (styleConfig.fontFamily) {
    document.documentElement.style.setProperty('--font-family', styleConfig.fontFamily)
  }
  
  // 应用自定义CSS
  if (styleConfig.customCSS) {
    const styleElement = document.getElementById('custom-css') || document.createElement('style')
    styleElement.id = 'custom-css'
    styleElement.textContent = styleConfig.customCSS
    document.head.appendChild(styleElement)
  }
}

onMounted(() => {
  // 初始应用配置样式
  applyConfigStyles(props.config.styleConfig || {})
  
  // 设置定时更新从API获取数据（每50毫秒更新一次）
  updateInterval = setInterval(() => {
    initializePlayersFromApi()
  }, 50)
})

onUnmounted(() => {
  // 清理定时器
  if (updateInterval) {
    clearInterval(updateInterval)
  }
  
  // 清理自定义CSS
  const customStyle = document.getElementById('custom-css')
  if (customStyle) {
    customStyle.remove()
  }
})
</script>



<style scoped>
/* 全局SVG图标样式 - 确保所有SVG都显示为白色 */
img[src$=".svg"] {
  filter: brightness(0) invert(1);
}

.fps-overlay {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: transparent;
  pointer-events: none;
  font-family: 'Arial', sans-serif;
  color: white;
}

/* 回合信息 */
.round-info {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333331; /* 设置为不透明 */
  border: 0px solid #333;
  border-radius: 9px;
  padding: 15px 30px;
  z-index: 100;
}

/* 左侧队伍颜色竖条 - 假设T方主色为红色 */
.round-info::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  background-color: #FFD700; /* T方主色 - 红色 */
  border-top-left-radius: 9px;
  border-bottom-left-radius: 9px;
}

/* 右侧队伍颜色竖条 - 假设CT方主色为蓝色 */
.round-info::after {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  background-color: #1E90FF; /* CT方主色 - 蓝色 */
  border-top-right-radius: 9px;
  border-bottom-right-radius: 9px;
}

.team-scores {
  display: flex;
  gap: 60px;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.team-logo {
  width: 45px;
  height: 45px;
  border-radius: 6px;
}

.team-name {
  font-weight: bold;
  font-size: 21px;
}

.team-score {
  font-size: 36px;
  font-weight: bold;
  color: white;
}

.round-timer {
  display: flex;
  align-items: center;
}

.round-number {
  font-size: 26px;
  font-weight: bold;
  color: white;
}

.progress-bar {
  width: 150px;
  height: 9px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4.5px;
  overflow: hidden;
}

.progress-fill {
  width: 60%;
  height: 100%;
  background-color: #4CAF50;
}

/* 玩家卡片 */
.t_player-cards {
  position: absolute;
  bottom: 20px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  z-index: 100;
}

.ct_player-cards {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  z-index: 100;
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.player-name {
  font-size: 20px;
}

.player-weapon {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 5px;
  opacity: 0.8;
}

.weapon-icon {
  width: 20px;
  height: 20px;
}

.health-bg {
    position: absolute;
    bottom: 0;
    left: 0;
    background-color: #4CAF50;
    opacity: 1;
    border-radius: 4px;
    z-index: 5;
    height: 33%;
    transition: all 0.5s ease-out;
  }

  /* 设置血条高度与player-health一致 */
.player-card.alive .health-bg {
  height: 100% !important;
  bottom: 0;
  left: 0;
  right: 0;
  margin: 0;
  padding: 0;
}

/* T队伍（右侧卡片）血条背景色 - 已互换 */
.player-card.alive.ct-card .health-bg {
  background-color: #336FDE;
}

/* CT队伍（左侧卡片）血条背景色 - 已互换 */
.player-card.alive.left-card .health-bg {
  background-color: #F1A136;
}

  /* 死亡选手血条样式 - 设为深灰色，确保完全不透明 */
  .player-card.dead .health-bg {
    background-color: #444444 !important;
    height: 100% !important;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 0;
    padding: 0;
    opacity: 1 !important;
  }

  .health-value {
    font-size: 20px;
    min-width: 30px;
    text-align: right;
    position: relative;
    z-index: 10;
    color: #ffffff;
    font-weight: bold;
  }
  
  /* 血量和护盾容器样式 */
  .health-with-shield {
    display: flex;
    align-items: center;
    gap: 2px;
    position: relative;
    z-index: 10;
  }
  
  /* 护盾容器样式 */
  .shield-container {
    position: relative;
    width: 24px;
    height: 24px;
  }

  /* 护盾图标样式 */
  .shield-icon {
    position: absolute;
    top: 0;
    left: 0;
    width: 24px;
    height: 24px;
    fill: #FFFFFF;
  }

  /* 头盔图标样式*/
  .helmet-icon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 16px;
    height: 16px;
    fill: #FFFFFF;
    z-index: 20;
  }
  
  /* 确保右侧卡片的血量值向右对齐 */
  .ct-card .health-value {
    text-align: right !important;
  }
  
  /* 右侧卡片的护盾容器位置调整 */
  .ct-card .shield-container {
    margin-left: 5px;
  }

.player-info {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 10px;
  opacity: 0.8;
  align-items: center;
}

/* 赞助商广告 */
.sponsor-banner {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 100;
}

.sponsor-banner svg {
  border-radius: 4px;
}

/* 调整玩家卡片样式 */
.t_player-cards {
  position: absolute;
  bottom: 20px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  z-index: 100;
}

.ct_player-cards {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  z-index: 100;
}

/* 玩家卡片基础样式和过渡效果 */
.player-card {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  background-color: rgba(0, 0, 0, 0.9);
  border-radius: 6px;
  padding: 5px;
  height: 90px;
  font-size: 36px;
  position: relative;
  overflow: hidden;
}

/* 存活玩家卡片样式 */
.player-card.alive {
  min-width: 300px;
  opacity: 1;
  transform: translateY(0);
}

/* 死亡玩家卡片样式 - 与存活玩家保持一致 */
.player-card.dead {
  min-width: 180px;
  opacity: 0.8;
  transform: translateY(10px);
}

/* 玩家名称过渡效果 */
.player-name {
  transition: color 0.5s ease;
}

/* 健康值过渡效果 */
.health-value {
  transition: all 0.5s ease;
}

/* 死亡卡片在血条中显示统计数据 */
.dead-stats-in-health {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  z-index: 10;
}

/* 死亡选手KD容器样式 */
.dead-kd {
  display: flex;
  align-items: center;
}

/* 死亡选手名称样式调整 */
.player-card.dead .player-name {
  color: #ccc;
}

/* ADR数据显示 */
.dead-adr {
  display: flex;
  align-items: center;
  gap: 4px;
}

.adr-value {
  font-size: 15px;
  color: #7c7c7c;
  font-weight: bold;
}

.adr-label {
  font-size: 12px;
  color: #7c7c7c;
  font-weight: bold;
}

/* 死亡选手KD显示 */
.player-card.dead .kd-value {
  color: #7c7c7c;
  font-weight: bold;
}

/* 死亡选手隐藏不需要的元素 */
.player-card.dead .player-weapon,
.player-card.dead .weapon-in-health,
.player-card.dead .health-value {
  display: none !important;
}

/* 左边卡片对齐样式 */
.left-card {
  text-align: left;
}

/* 右边卡片对齐样式 */
.ct-card {
  text-align: right;
}

/* 为死亡卡片添加特殊的透明度效果 */
.player-card.dead .player-header {
  opacity: 0.8;
}

/* 优化左右卡片的对齐和布局 */
.t_player-cards {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.ct_player-cards {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

/* 右边卡片内元素位置左右互换 */
.ct-card .player-header {
  flex-direction: row-reverse;
}

.ct-card .kd-display {
  margin-right: 0;
  margin-left: 5px;
}

/*血条样式 */
.player-health {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 6px;
  height: 33%;
  z-index: 20; /* 增加z-index确保血条在player-card的最上层 */
  background-color: rgba(0, 0, 0, 1);
}
.player-eco {
  display: block;
  font-size: 15px;
  font-weight: bold;
  color: #1fcf45;
}

.weapon-in-health {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  color: #fff;
  position: relative;
  z-index: 10;
}

.weapon-in-health .weapon-icon {
  width: 24px;
  height: 24px;
}

/* 右边卡片武器信息和血量值位置调整 - 对存活选手保持space-between，对死亡选手特殊处理 */
.ct-card .player-health {
  flex-direction: row;
  justify-content: space-between;
}

/* 左侧卡片武器图标与武器名位置互换 */
.left-card .weapon-in-health {
  flex-direction: row-reverse;
}

/* 死亡选手卡片血量条中的统计数据居中显示 */
.player-card.dead .player-health {
  justify-content: center;
}

/* 右侧死亡卡片在血条中显示统计数据的布局调整 - 保持居中对齐 */
.player-card.dead.ct-card .dead-stats-in-health {
  justify-content: center;
}

/* 隐藏原有的武器区域 */
.player-weapon {
  display: none;
}

/* KD显示样式 */
   .kd-display {
      display: flex;
      align-items: center;
    }

    .kd-icon {
      margin-left: 4px;
      width: 16px;
      height: 16px;
      vertical-align: middle;
    }

    .kd-values {
      display: flex;
      flex-direction: row;
      align-items: center;
    }

    .kd-value {
      font-size: 16.5px;
      color: #ffffff;
      min-width: 22.5px;
      text-align: center;
    }

  .kd-label {
    font-size: 11px;
    color: #FFD700;
    font-weight: bold;
    display: none; /* 隐藏KD标签 */
  }

  .player-stats {
    display: none;
  }

  .player-score {
    display: none;
  }

  .player-info {
    display: none; /* 隐藏玩家信息区域 */
  }
</style>